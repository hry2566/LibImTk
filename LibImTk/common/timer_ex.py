import threading
import time

class TimerEx:
    def __init__(self, interval_ms:int=None, callback:callable=None):
        self.__interval = interval_ms / 1000 if interval_ms is not None else None
        self.__callback = callback
        self.__is_running = False
        self.__timer_thread = None
        self.__start_time = None

    def __timer_loop(self):
        self.__start_time = time.perf_counter()
        next_call_time = self.__start_time

        while self.__is_running:
            next_call_time += self.__interval

            while time.perf_counter() < next_call_time:
                remaining_time = next_call_time - time.perf_counter()
                if remaining_time > 0:
                    time.sleep(remaining_time)
            try:
                elapsed = time.perf_counter() - self.__start_time
                if self.__callback:
                    self.__callback(elapsed * 1000)
            except Exception as e:
                print(f"Error in timer callback: {e}")

    def start(self):
        if not self.__is_running:
            self.__is_running = True
            self.__timer_thread = threading.Thread(target=self.__timer_loop, daemon=True)
            self.__timer_thread.start()
            print(f"BusyLoopTimer started. Interval: {self.__interval * 1000:.2f}ms")

    def stop(self):
        if self.__is_running:
            self.__is_running = False
            if self.__timer_thread and self.__timer_thread.is_alive():
                self.__timer_thread.join()
                print("BusyLoopTimer stopped.")

    def after(self, delay_ms: float, callback: callable, *args: tuple):
        """
        指定時間後にコールバックを1回だけ呼び出す（elapsed付き）。
        
        Args:
            delay_ms (float): 遅延時間（ミリ秒）。
            callback (callable): 実行する関数。
            *args: コールバック関数に渡す引数。
        """
        delay_sec = delay_ms / 1000
        start_time = time.perf_counter()

        def run_after():
            time.sleep(delay_sec)
            try:
                elapsed = time.perf_counter() - start_time
                callback(elapsed * 1000, *args)
            except Exception as e:
                print(f"Error in after() callback: {e}")
        threading.Thread(target=run_after, daemon=True).start()

if __name__ == '__main__':
    def repeated(elapsed_ms):
        print(f"[Repeated] {elapsed_ms:.2f}ms")

    def one_shot(elapsed_ms, *args):
        print(f"[After] One-time callback fired after {elapsed_ms:.2f}ms")
        print(f"Received arguments: {args}")

    timer = TimerEx(1000, repeated)
    timer.start()

    timer.after(3000, one_shot, "arg1", 123)

    time.sleep(6)
    timer.stop()