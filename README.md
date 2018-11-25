# urb-piper-foogg

### Project Overview
Consider yourself as one of the core developers of a reputed food aggregator platform. With a surge in people ordering food, your team has been facing a lot of issues handling the delivery of food orders efficiently. So far, it has all been done manually—
An order is received at a store, the store manager calls a delivery support center for a delivery boy, a delivery boy is assigned, who then shows up and delivers the order.
With scale, the above approach is no longer feasible.
You are now entrusted to build a system that can robustly scale and manage these deliveries in an efficient and automated manner.

### The problem statement
Create a scalable delivery task processing system.
To help you build the system, here are some inputs that you can keep in mind:

Types and their attributes:
* Delivery task
* Title (string)
* Priority – can be one of high, medium, low
* Creation date-time
* Created by – reference to the person who created the task.
* Store manager – can create delivery tasks.
* Delivery person – accepts and acts upon tasks.

### Things to do
Provide a simple web interface for logging-in of store managers and delivery persons.

When a Store manager logs-in, he/she can:
* create a task
* view the list of past tasks and their last known state
* click on a task to see its various state transitions
* cancel a task which is not yet accepted

When a delivery person logs-in, he/she can:
* view any previous task that has been accepted by the current logged-in person
* decline any previously accepted task, which hasn’t been completed as yet.
* complete any previously accepted task.
* view a single, highest priority task (the logic for this will be explained below) from the available tasks in the task queue.
* accept a task from the task queue (NOTE: a delivery person can’t have more than 3 tasks in the pending state)

A delivery task can have multiple states associated with it. 
* new – task has been created but not accepted
* accepted – task has been accepted by a delivery person
* completed – task has been completed
* declined – task has been declined by the delivery person. Once declined, a task moves to the new state again and any other delivery person can accept it.
* cancelled – task has been cancelled by store manager

Tasks created by the store manager should be visible (if applicable as per priority) to logged-in delivery persons in real-time.

If a task is declined by a delivery person, an alert should be visible to the store manager in real-time.

If a task has been accepted by a delivery person, then it should not be visible for acceptance to any other logged-in delivery person in real-time.

#### Logic for task visibility:
All tasks that are in the new state, should be maintained in a queue. Tasks should be visible for acceptance on the basis of their priority. A high priority task is more important than a medium priority task, which in-turn is more important than low priority task.
NOTE: all logged-in delivery persons should see only 1 task, which has the highest priority as of that moment. Once accepted, the visible task should be refreshed in real-time to show the next highest priority task.

### Running the App locally

> Python v3.6+ is required, and use of a virtual env is recommended

#### Stacks used:
1. Flask (Restful)
2. MongoDB
3. VueJS
4. RabbitMQ for priority task queue
5. Flask-SocketIO for real time websocket updates

#### Backend (Dev mode):
```bash
$ pip install gunicorn eventlet
$ pip install -r requirements.txt
$ python users.py
$ gunicorn run:application --log-level=debug --reload --worker-class eventlet -w 1 
```
#### Frontend (Vue - Yarn):
```bash
$ cd foog_ui
$ yarn install
$ yarn serve
```