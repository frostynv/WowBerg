"""Main entrypoint for non-HTTP startup tasks."""

import threading

from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.services.auction import AuctionDataService
from wowberg.debug.debug import DebugInterface

LOCALE = "en_US"
UPDATE_INTERVAL_SECONDS = 3600 # 30 minutes in seconds, the recommended polling interval for Blizzard auction data


class WowBerg(DebugInterface):
    def __init__(self) -> None:
        super().__init__()
        # Persistent data storage for WowBerg, such as cached auction data and metadata.
        self._persistance_data = {"services": {}}
        self._scheduler = self.WowBergScheduler()

    def run_wowberg(self) -> None:
        """Start the Blizzard update flow in the background and keep process alive."""
        self.debugger.log("===== Welcome to WowBerg =====")

        self._scheduler.start(tasks={"update_auction_data": self.run_update_db})

        # Keep main thread alive and handle graceful shutdown
        try:
            while not self._scheduler._stop_event.is_set():
                self._scheduler._stop_event.wait(1)
        except KeyboardInterrupt:
            self._scheduler.stop()
            self.debugger.log(
                "Scheduler shutting down",
                prefix=DebugInterface.ErrorLevels.INFO,
            )

        self.debugger.log("===== Bye WowBerg =====")
        self.pre_shutdown()

    def pre_shutdown(self) -> None:
        """Stop the scheduler and perform any necessary cleanup."""
        self._scheduler.wait_for_shutdown()

    class WowBergScheduler(DebugInterface):
        def __init__(self, name: str = "WowBergScheduler"):
            super().__init__()
            self._name = name
            self._stop_event = threading.Event()
            self._scheduler_thread: threading.Thread | None = None
            self._task_lock = (
                threading.Lock()
            )  # Ensure only one update task runs at a time
            self._tasks = {}

        def _run_scheduler(
            self, interval_seconds: int, tasks: dict[str, callable] = None
        ) -> None:
            """Execute update work repeatedly at the configured interval."""
            while not self._stop_event.is_set():
                try:
                    self._run_tasks(tasks)
                except Exception as e:
                    self.debugger.log(
                        f"Error occurred: {e}",
                        prefix=DebugInterface.ErrorLevels.CRITICAL,
                    )

                # case: wait for configured interval
                # case: if stop event is set, activate thread, and break current loop to stop scheduler
                if self._stop_event.wait(interval_seconds):
                    break

        def _run_tasks(self, tasks: dict[str, callable]) -> None:
            """Run a specific task by name."""
            if not tasks:
                self.debugger.log(
                    "No tasks provided to scheduler.",
                    prefix=DebugInterface.ErrorLevels.WARN,
                )
                return

            for task_name, task_func in tasks.items():
                with self._task_lock:
                    self.debugger.log(
                        f"Task started: {task_name}",
                        prefix=DebugInterface.ErrorLevels.INFO,
                    )
                    try:
                        task_func()
                        self.debugger.log(
                            f"Task completed: {task_name}",
                            prefix=DebugInterface.ErrorLevels.INFO,
                        )
                    except Exception as e:
                        self.debugger.log(
                            f"Error in task '{task_name}': {e}",
                            prefix=DebugInterface.ErrorLevels.CRITICAL,
                        )

        def start(
            self, interval_seconds: int = UPDATE_INTERVAL_SECONDS, tasks=None
        ) -> None:
            """Run updates on a background loop without blocking the caller thread."""

            # Guard: Singleton thread for scheduler
            if self._scheduler_thread and self._scheduler_thread.is_alive():
                self.debugger.log(
                    "Scheduler is already running. No action taken.",
                    prefix=DebugInterface.ErrorLevels.WARN,
                )
                return
            # Reset the stop event
            self._stop_event.clear()
            # Create and start the thread for the scheduler loop
            self._scheduler_thread = threading.Thread(
                target=self._run_scheduler,
                args=(interval_seconds, tasks),
                name="wowberg-auction-updater",
                daemon=True,
            )
            self.debugger.log(
                f"Running {self._name} \n | Interval: {interval_seconds} seconds \n | Tasks: {list(tasks.keys()) if tasks else 'EMPTY'} ",
                prefix=DebugInterface.ErrorLevels.INFO,
            )
            self._scheduler_thread.start()

        def stop(self) -> None:
            """Signal the background scheduler loop to stop."""
            # Flag: wakes scheduler thread
            self._stop_event.set()

        def wait_for_shutdown(self) -> None:
            """Keep process alive until interrupted, then stop scheduler cleanly."""
            try:
                while not self._stop_event.is_set():
                    self._stop_event.wait(1)
            except KeyboardInterrupt:
                self.stop()
                self.debugger.log(
                    "Scheduler shutting down",
                    prefix=DebugInterface.ErrorLevels.INFO,
                )

    def run_update_db(self) -> None:
        """Fetch and log the Blizzard OAuth token."""
        blizzard_client = BlizzardOAuthClient(region=BlizzardRegions.US)

        try:
            blizzard_client.authenticate()
        except Exception as e:
            self.debugger.log(
                f"Token Service: {e}",
                prefix=DebugInterface.ErrorLevels.CRITICAL,
            )
            return

        self.fetch_and_export_auctions(
            blizzard_client=blizzard_client,
            region=BlizzardRegions.US,
            realm_name="ursin",
        )

    def fetch_and_export_auctions(
        self,
        blizzard_client: BlizzardOAuthClient,
        region: BlizzardRegions,
        realm_name: str,
    ) -> None:
        # second test fetching from auction data
        auction_service = AuctionDataService(client=blizzard_client)
        try:
            auction_service.update_all_auctions(
                region=region, realm_name=realm_name, cached=True
            )
        except Exception as e:
            self.debugger.log(
                f"Auction Service: {e}",
                prefix=DebugInterface.ErrorLevels.CRITICAL,
            )
            return

        last_modified = auction_service.data_last_modified
        auction_data = auction_service._data.get("data", "")
        filename = f"./export_json/{region}_{realm_name}_{last_modified}.json"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(auction_data)
            self.debugger.log(
                f"File created: {filename}",
                prefix=DebugInterface.ErrorLevels.INFO,
            )
        except Exception as e:
            self.debugger.log(
                f"Error exporting auction data: {e}",
                prefix=DebugInterface.ErrorLevels.CRITICAL,
            )


if __name__ == "__main__":
    wowberg = WowBerg()
    wowberg.run_wowberg()
