"""Main entrypoint for non-HTTP startup tasks."""

import threading

from wowberg.blizzard_oath_client import BlizzardOAuthClient, BlizzardRegions
from wowberg.services.auction import AuctionDataService
from wowberg.logger import Logger
from wowberg.schema import init_db

LOCALE = "en_US"
UPDATE_INTERVAL_SECONDS = 600  # 30 minutes in seconds, the recommended polling interval for Blizzard auction data

class WowBerg:
    def __init__(self) -> None:
        # Persistent data storage for WowBerg, such as cached auction data and metadata.
        self._persistance_data = {"services": {}}
        self._scheduler = self.WowBergScheduler()
        self._module_data = self.WowBergData()

    def run_wowberg(self) -> None:
        """Start the Blizzard update flow in the background and keep process alive."""
        Logger.log("===== Welcome to WowBerg =====")

        init_db()
        self._scheduler.start(
            tasks={"update_auction_data": self._module_data.run_update_auctions}
        )

        # Keep main thread alive and handle graceful shutdown
        try:
            while not self._scheduler._stop_event.is_set():
                self._scheduler._stop_event.wait(1)
        except KeyboardInterrupt:
            self._scheduler.stop()
            Logger.log(
                "Scheduler shutting down",
                prefix=Logger.ErrorLevels.INFO,
            )

        Logger.log("===== Bye WowBerg =====")
        self.shutdown_wowberg()

    def shutdown_wowberg(self) -> None:
        """Stop the scheduler and perform any necessary cleanup."""
        self._scheduler.wait_for_shutdown()

    class WowBergScheduler:
        def __init__(self, name: str = "WowBergScheduler"):
            self._name = name
            self._stop_event = threading.Event()
            self._scheduler_thread: threading.Thread | None = None
            self._task_lock = (
                threading.Lock()
            )  # Ensure only one update task runs at a time
            self._tasks = {}
            
            
        def start(
            self, interval_seconds: int = UPDATE_INTERVAL_SECONDS, tasks=None
        ) -> None:
            """Initialize and run updates on a background loop without blocking the caller thread."""

            # Guard: Singleton thread for scheduler
            if self._scheduler_thread and self._scheduler_thread.is_alive():
                Logger.log(
                    "Scheduler is already running. No action taken.",
                    prefix=Logger.ErrorLevels.WARN,
                )
                return
            # Reset the stop event
            self._stop_event.clear()
            # Create and start the thread for the scheduler loop
            self._scheduler_thread = threading.Thread(
                target=self._run,
                args=(interval_seconds, tasks),
                name="wowberg-auction-updater",
                daemon=True,
            )
            Logger.log(
                f"Running {self._name} \n | Interval: {interval_seconds} seconds \n | Tasks: {list(tasks.keys()) if tasks else 'EMPTY'} ",
                prefix=Logger.ErrorLevels.INFO,
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
                Logger.log(
                    "Scheduler shutting down",
                    prefix=Logger.ErrorLevels.INFO,
                )

        def _run(
            self, interval_seconds: int, tasks: dict[str, callable] = None
        ) -> None:
            """Execute update work repeatedly at the configured interval."""
            while not self._stop_event.is_set():
                try:
                    self._run_tasks(tasks)
                except Exception as e:
                    Logger.log(
                        f"Error occurred: {e}",
                        prefix=Logger.ErrorLevels.CRITICAL,
                    )

                # case: wait for configured interval
                # case: if stop event is set, activate thread, and break current loop to stop scheduler
                if self._stop_event.wait(interval_seconds):
                    break

        def _run_tasks(self, tasks: dict[str, callable]) -> None:
            """
            Execute list of tasks sychronously
            """

            # guard: no tasks provided
            if not tasks:
                Logger.log(
                    "No tasks provided to scheduler.",
                    prefix=Logger.ErrorLevels.WARN,
                )
                return

            for task_name, task_func in tasks.items():
                with self._task_lock:
                    Logger.log(
                        f"Task started: {task_name}",
                        prefix=Logger.ErrorLevels.INFO,
                    )
                    try:
                        task_func()
                        Logger.log(
                            f"Task completed: {task_name}",
                            prefix=Logger.ErrorLevels.INFO,
                        )
                    except Exception as e:
                        Logger.log(
                            f"Error in task '{task_name}': {e}",
                            prefix=Logger.ErrorLevels.CRITICAL,
                        )


    class WowBergData:
        def run_update_auctions(self) -> None:
            """Fetch and log the Blizzard OAuth token."""
            blizzard_client = BlizzardOAuthClient(region=BlizzardRegions.US)

            try:
                blizzard_client.authenticate()
            except Exception as e:
                Logger.log(
                    f"Token Service: {e}",
                    prefix=Logger.ErrorLevels.CRITICAL,
                    handler="blizzard",
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
            """
            In a function mainly to export the auction data to a file
            """
            
            # second test fetching from auction data
            auction_service = AuctionDataService(client=blizzard_client)
            try:
                auction_service.update_all_auctions(
                    region=region, realm_name=realm_name, cached=True
                )
            except Exception as e:
                Logger.log(
                    f"Auction Service: {e}",
                    prefix=Logger.ErrorLevels.CRITICAL,
                    handler="blizzard",
                )
                return

            last_modified = auction_service.data_last_modified
            auction_data = auction_service._data.get("data", "")
            filename = (
                f"./export_json/{region}_{realm_name}_{last_modified}.json"
            )
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(auction_data)
                Logger.log(
                    f"File created: {filename}",
                    prefix=Logger.ErrorLevels.INFO,
                    handler="blizzard",
                )
            except Exception as e:
                Logger.log(
                    f"Error exporting auction data: {e}",
                    prefix=Logger.ErrorLevels.CRITICAL,
                    handler="blizzard",
                )


if __name__ == "__main__":
    wowberg = WowBerg()
    wowberg.run_wowberg()
