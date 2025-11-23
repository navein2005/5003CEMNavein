import time     # We'll need this for all our timing tests
import threading # We'll need this for the multithreading part
import math     # Using math.factorial to check our work (optional)

# --- Step 1: Factorial Function (Q3.2) ---

def calculate_factorial(n):
    """
    Calculates the factorial of a number 'n' using an iterative loop.
    Stores the result in a shared list (for threading).
    """
    result = 1
    for i in range(1, n + 1):
        result = result * i
    # We don't print here to avoid I/O slowing down the test
    # Instead, we just return the result
    return result


# --- Step 2: Multithreaded Program (Q3.3) ---

def run_multithreaded_test():
    """
    Runs the factorial calculations (50, 100, 200) using 3 separate threads.
    Repeats this 10 times and calculates the average time.
    """
    print("--- Starting Multithreaded Test (10 rounds) ---")
    numbers_to_test = [50, 100, 200]
    total_times = []

    for i in range(10):  # Perform testing in 10 rounds
        threads = []

        # Get the start time of the *first* thread to be created
        start_time = time.time_ns()

        # Create 3 separate threads, one for each number
        for num in numbers_to_test:
            # We must pass 'num' as an argument in a tuple
            thread = threading.Thread(target=calculate_factorial, args=(num,))
            threads.append(thread)
            thread.start()  # Start the thread

        # Wait for all 3 threads to complete their execution
        for thread in threads:
            thread.join()

        # Get the end time *after* the *last* thread has finished
        end_time = time.time_ns()

        # Calculate the total time elapsed for this round
        time_elapsed = end_time - start_time
        total_times.append(time_elapsed)

        print(f"Round {i + 1}: {time_elapsed} ns")

    # Calculate and print the average time
    average_time = sum(total_times) / len(total_times)
    print(f"\nMultithreaded Average Time: {average_time:.0f} ns")
    return average_time


# --- Step 3: Sequential Program (Q3.4) ---

def run_sequential_test():
    """
    Runs the factorial calculations (50, 100, 200) sequentially.
    Repeats this 10 times and calculates the average time.
    """
    print("\n--- Starting Sequential Test (10 rounds) ---")
    numbers_to_test = [50, 100, 200]
    total_times = []

    for i in range(10):  # Perform testing in 10 rounds

        # Get the start time
        start_time = time.time_ns()

        # Run the calculations one after another in the main thread
        for num in numbers_to_test:
            calculate_factorial(num)

        # Get the end time
        end_time = time.time_ns()

        # Calculate the total time elapsed for this round
        time_elapsed = end_time - start_time
        total_times.append(time_elapsed)

        print(f"Round {i + 1}: {time_elapsed} ns")

    # Calculate and print the average time
    average_time = sum(total_times) / len(total_times)
    print(f"\nSequential Average Time: {average_time:.0f} ns")
    return average_time


# --- Step 4: Run Both Tests and Analyze ---

if __name__ == "__main__":
    mt_avg = run_multithreaded_test()
    seq_avg = run_sequential_test()

    print("\n================== FINAL RESULTS ==================")
    print(f"  Sequential Average Time: {seq_avg:.0f} ns")
    print(f"  Multithreaded Average Time: {mt_avg:.0f} ns")

    if mt_avg < seq_avg:
        print("\nConclusion: Multithreading was FASTER.")
        print(f"It was {seq_avg / mt_avg:.2f} times faster.")
    else:
        print("\nConclusion: Sequential was FASTER.")
        print(f"It was {mt_avg / seq_avg:.2f} times faster.")
