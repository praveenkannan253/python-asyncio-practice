# Python Asyncio: Revision Notes (with Code)

> Source: "What is Asyncio?" video (transcript covers up to **TaskGroup, ~16:49**).
> Python version: **3.11+** (TaskGroup was added in 3.11).
> Note: the auto-captions say "code routine", which is actually **coroutine**. "async output run" means `asyncio.run`.

---

## 1. What is Asyncio?

**Synchronous programming:** tasks run one after another (A → B → C → D). If one task is delayed, everything else waits.

**Asynchronous programming:** you can start tasks B, C, D even if task A has not finished yet.

**Real-world example (chai kadai):**
- Sync master: paal kaachum varaikkum waiting, next customer-ah kandukkave maatan.
- Async master: paal kaachum bodhu, next order eduthu cup ready pannuvan. Waiting time waste aagaadhu.

> **Key idea:** Use the waiting time to do other work. Best for tasks with lots of waiting and little CPU work.

---

## 2. When to use what?

| Model | Best for | Examples |
|---|---|---|
| **asyncio** | Many waiting tasks (I/O bound), low CPU usage | API calls, file reads, DB queries |
| **Threads** | I/O bound tasks that share data | Background downloads sharing state |
| **Processes** | CPU-heavy tasks, true parallelism across cores | Image processing, ML training, heavy maths |

> **I/O** = Input/Output (network, disk).

---

## 3. Key concepts (the video covers 1, 2 and 3 here)

### Concept 1: Event Loop

**Definition:** The event loop is the core of asyncio. It manages and schedules tasks, running them one at a time and switching whenever a task is waiting.

- When a task hits `await`, it steps aside and another task runs.
- When the awaited operation completes, the task resumes.

**Real-world:** Traffic signal maari. Oru lane block-na, vera lane-ku green kudukkum.

---

### Concept 2: Coroutines

**Definition:**
- **Coroutine function:** a function defined with `async def`.
- **Coroutine object:** what you get when you *call* a coroutine function. It does not execute until it is awaited or wrapped in a task.

**Steps:**
1. `import asyncio` (built-in, no installation needed)
2. Define a function with `async def`
3. Run it with `asyncio.run(main())`, which starts the event loop

```python
import asyncio

async def main():
    print("Start of main coroutine")

asyncio.run(main())
```

#### Common trap: calling does not run it

```python
async def main():
    print("Start of main coroutine")

main()         # RuntimeWarning: coroutine 'main' was never awaited
print(main())  # <coroutine object main at 0x...>
```

#### The `await` keyword

**Definition:** `await` pauses the current coroutine until the awaited coroutine, task or future finishes, then gives you its result. It can only be used **inside an `async` function**.

```python
import asyncio

async def fetch_data(delay):
    print("Fetching data...")
    await asyncio.sleep(delay)   # simulates an I/O wait
    print("Data fetched")
    return {"data": "Some data"}

async def main():
    print("Start of main coroutine")
    coro = fetch_data(2)         # only a coroutine object, NOT running yet
    result = await coro          # now it runs, and we wait for it
    print(f"Received result: {result}")
    print("End of main coroutine")

asyncio.run(main())
```

**Output:**
```
Start of main coroutine
Fetching data...
Data fetched
Received result: {'data': 'Some data'}
End of main coroutine
```

#### Trap: creating is not running

```python
async def main():
    print("Start of main coroutine")
    coro = fetch_data(2)
    print("End of main coroutine")    # prints BEFORE fetching starts
    result = await coro               # fetching happens here
    print(f"Received result: {result}")
```

Order: Start → End → Fetching → Fetched → Result. The coroutine only started at the `await` line.

#### Trap: awaiting two coroutines one by one gives no speed benefit

```python
async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id}

async def main():
    coro1 = fetch_data(1, 2)
    coro2 = fetch_data(2, 2)

    result1 = await coro1     # waits 2 sec
    print(result1)
    result2 = await coro2     # waits another 2 sec
    print(result2)

asyncio.run(main())
# Total = ~4 seconds (no benefit)
```

> A coroutine does not start until it is awaited, so the second one only starts after the first finishes.

---

### Concept 3: Tasks

**Definition:** A task wraps a coroutine and schedules it to run as soon as possible on the event loop. Multiple tasks run **concurrently**.

- Concurrent does not mean parallel. Only one task runs at a time (single CPU core), but when one task is idle, the loop switches to another.

#### 3a. `asyncio.create_task()`

```python
import asyncio

async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}

async def main():
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 3))
    task3 = asyncio.create_task(fetch_data(3, 1))

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)

asyncio.run(main())
# Sequential: 2 + 3 + 1 = 6 sec
# With tasks: ~3 sec (the longest task)
```

> **Total time = the longest task**, not the sum.

If you want to control the order (for example, start task 3 only after tasks 1 and 2 finish), `await` them first:

```python
task1 = asyncio.create_task(fetch_data(1, 2))
task2 = asyncio.create_task(fetch_data(2, 3))
result1 = await task1
result2 = await task2

task3 = asyncio.create_task(fetch_data(3, 1))   # starts after 1 and 2 are done
result3 = await task3
```

---

#### 3b. `asyncio.gather()`

**Definition:** `gather()` runs multiple coroutines concurrently and returns their results as a **list, in the same order you passed them**.

```python
import asyncio

async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}

async def main():
    results = await asyncio.gather(
        fetch_data(1, 2),
        fetch_data(2, 1),
        fetch_data(3, 3),
    )

    for result in results:
        print(f"Received result: {result}")

asyncio.run(main())
# Total ~3 sec
```

**Limitation:** weak error handling. If one coroutine fails, the others are **not automatically cancelled**, which can leave your app in an inconsistent state unless you handle exceptions manually.

---

#### 3c. `asyncio.TaskGroup` (3.11+, preferred)

**Definition:** `TaskGroup` is an async context manager that groups tasks together with built-in error handling. If any task fails, all the other tasks in the group are cancelled automatically.

```python
import asyncio

async def fetch_data(id, delay):
    print(f"Fetching data for id {id}")
    await asyncio.sleep(delay)
    print(f"Data fetched for id {id}")
    return {"id": id, "data": f"Sample data from coroutine {id}"}

async def main():
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for i, delay in enumerate([2, 1, 3], start=1):
            task = tg.create_task(fetch_data(i, delay))
            tasks.append(task)

    # By here, all tasks have finished
    results = [task.result() for task in tasks]
    for result in results:
        print(f"Received result: {result}")

asyncio.run(main())
```

> When the `async with` block exits, all tasks are already complete. Cleaner and safer than `gather`.

---

## 4. gather vs TaskGroup

| Feature | `gather()` | `TaskGroup` |
|---|---|---|
| Runs concurrently | Yes | Yes |
| Python version | Older versions too | 3.11+ |
| Error handling | Weak, others not auto-cancelled | Built-in, others auto-cancelled |
| Results | List in the same order | `task.result()` per task |
| Best for | Simple cases | Larger, more robust apps |

---

## 5. Quick cheat sheet

```python
import asyncio

# Define a coroutine function
async def work(): ...

# Entry point (starts the event loop)
asyncio.run(work())

# Wait for one coroutine
result = await work()

# Schedule a task (starts now)
t = asyncio.create_task(work())

# Run many, get a list of results
results = await asyncio.gather(work(), work())

# Run many, with safe error handling (3.11+)
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(work())
    t2 = tg.create_task(work())
```

**Memory tips:**
- `async def` = coroutine function. Calling it gives a coroutine object.
- A coroutine object does nothing until it is **awaited** or **wrapped in a task**.
- `await` means "wait here, let other tasks run meanwhile."
- Use `asyncio.sleep()`, not `time.sleep()`. The second one blocks the whole event loop.

---

## 6. Interview Q&A (with answers)

**Q1. What is asyncio and when do you use it?**
A: Asyncio is Python's library for writing concurrent code using `async`/`await` on a single thread. It is best for I/O-bound work (network calls, file reads, DB queries) because other tasks can run while one is waiting.

**Q2. Asyncio vs threads vs processes?**
A: Asyncio: single thread, cooperative switching, best for I/O-bound work. Threads: shared memory, good for I/O-bound work, but the GIL limits CPU parallelism. Processes: separate memory, multiple cores, best for CPU-bound work.

**Q3. What is the event loop?**
A: The core component that schedules and runs tasks. When a task awaits, the loop pauses it and runs another task, then resumes the first when its wait is over.

**Q4. Coroutine function vs coroutine object?**
A: A function defined with `async def` is a coroutine function. Calling it does not execute it. It returns a coroutine object, which must be awaited or wrapped in a task to run.

**Q5. Why do you get "coroutine was never awaited"?**
A: You called an async function but never awaited the result. Fix it with `await func()` or `asyncio.create_task(func())`.

**Q6. What does `await` do, and where can you use it?**
A: It suspends the current coroutine until the awaited coroutine, task or future completes, and returns its result. It can only be used inside an `async def` function.

**Q7. If you await two coroutines one after another, do they run concurrently?**
A: No. The second starts only after the first finishes (sequential). For concurrency, use `create_task`, `gather` or `TaskGroup`.

**Q8. What is a task and how does `create_task` work?**
A: A task wraps a coroutine and schedules it on the event loop. `create_task` makes it start running right away. You `await` the task when you need the result.

**Q9. Concurrency vs parallelism?**
A: Concurrency means multiple tasks make progress by interleaving, even on one core. Parallelism means tasks run at the exact same time on multiple cores. Asyncio is concurrent, not parallel.

**Q10. `gather` vs `TaskGroup`?**
A: Both run concurrently. `gather` returns results as an ordered list, but if one coroutine fails the others are not automatically cancelled. `TaskGroup` (3.11+) cancels the remaining tasks on failure, so it is safer.

**Q11. Can you use `time.sleep()` inside an async function?**
A: No. It is blocking, so it freezes the thread and the whole event loop. Use `await asyncio.sleep()` instead.

**Q12. Three tasks of 2s, 3s and 1s run concurrently. Total time?**
A: About 3 seconds (the longest task). Sequentially it would be 6 seconds.

**Q13. What does `asyncio.run()` do?**
A: It creates an event loop, runs the given coroutine until it completes, then closes the loop. It is the usual program entry point.

**Q14. What happens if you run a CPU-heavy task in asyncio?**
A: It blocks the event loop, so all other tasks stall. For CPU-bound work use `multiprocessing` or `ProcessPoolExecutor`.

---

## 7. Revision checklist

- [ ] Can explain sync vs async
- [ ] Know when to use asyncio, threads, processes
- [ ] Can explain the event loop
- [ ] Know coroutine function vs coroutine object
- [ ] Know why "never awaited" happens
- [ ] Can write sequential `await` vs `create_task` code
- [ ] Know the difference between `gather` and `TaskGroup`
- [ ] Know `time.sleep` vs `asyncio.sleep`

---

## 8. Pending

The transcript **cuts off at 16:49**. The video mentions "five key concepts", but only **1 to 3** are covered here. Paste the remaining transcript to extend these notes.
