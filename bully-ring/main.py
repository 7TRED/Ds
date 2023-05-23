import time
import random
import threading


class BullyAlgorithm:
    def __init__(self, process_id, total_processes):
        self.process_id = process_id
        self.total_processes = total_processes
        self.coordinator = None
        self.election_in_progress = False

    def run(self):
        while True:
            if not self.coordinator:
                self.start_election()

            else:
                break
            time.sleep(5)

    def start_election(self):
        if not self.election_in_progress:
            print(f"Process {self.process_id}: Election started")
            self.election_in_progress = True
            for i in range(self.process_id + 1, self.total_processes + 1):
                if self.send_election_message(i):
                    self.election_in_progress = False
                    return
            self.declare_coordinator()

    def send_election_message(self, destination):
        print(
            f"Process {self.process_id}: Sending election message to process {destination}"
        )
        return random.choice([True, False])  # Simulating network communication

    def declare_coordinator(self):
        self.coordinator = self.process_id
        print(f"Process {self.process_id}: I am the new coordinator")


class RingAlgorithm:
    def __init__(self, process_id, total_processes):
        self.process_id = process_id
        self.total_processes = total_processes
        self.coordinator = None
        self.next_process = (process_id % total_processes) + 1

    def run(self):
        while True:
            if not self.coordinator:
                self.start_election()

            else:
                break

            time.sleep(5)

    def start_election(self):
        print(f"Process {self.process_id}: Election started")
        if self.process_id == 1:
            self.send_election_message(self.next_process)

    def send_election_message(self, destination):
        print(
            f"Process {self.process_id}: Sending election message to process {destination}"
        )
        if destination == self.process_id:
            self.declare_coordinator()
        else:
            self.next_process = (self.next_process % self.total_processes) + 1
            self.send_election_message(self.next_process)

    def declare_coordinator(self):
        self.coordinator = self.process_id
        print(f"Process {self.process_id}: I am the new coordinator")


if __name__ == "__main__":
    total_processes = 5
    process_id = 3

    bully_algorithm = BullyAlgorithm(process_id, total_processes)
    bully_thread = threading.Thread(target=bully_algorithm.run)

    ring_algorithm = RingAlgorithm(process_id, total_processes)
    ring_thread = threading.Thread(target=ring_algorithm.run)

    bully_thread.start()
    ring_thread.start()
