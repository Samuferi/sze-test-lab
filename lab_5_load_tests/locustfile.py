import random
from locust import HttpUser, task, between

class TodoUser(HttpUser):
    # Simulate a wait time between 1 and 2.5 seconds after each task
    wait_time = between(1, 2.5)

    def on_start(self):
        """
        This method is called when a simulated user starts.
        We can use it to initialize any data we need.
        """
        self.created_todo_ids = []
    
    # This task will be executed 3 times as often as other tasks (due to weight=3)
    @task(3)
    def get_all_todos(self):
        """
        Simulates a user fetching the list of all todos.
        """
        self.client.get("/todos", name="/todos (GET)")

    @task(2)
    def get_single_todo(self):
        """
        Simulates a user fetching a single, existing todo item.
        We'll just pick from the initial two IDs.
        """
        todo_id = random.choice([1, 2]+self.created_todo_ids)
        self.client.get(f"/todos/{todo_id}", name="/todos/{id} (GET)")

    @task(1)
    def create_todo(self):
        """
        Simulates a user creating a new todo item.
        """
        new_task_name = f"New task from user {random.randint(1, 1000)}"
        response = self.client.post(
            "/todos",
            json={"task": new_task_name},
            name="/todos (POST)"
        )

        if response.status_code == 201:
            created_todo = response.json()
            self.created_todo_ids.append(created_todo["id"])


    @task(1)
    def update_todo(self):
        """
        Simulates a user updating an existing todo item.
        We'll pick one of the first two items and toggle its 'done' status.
        """
        todo_id_to_update = random.choice(self.created_todo_ids + [1, 2])
        new_done_status = random.choice([True, False])
        
        self.client.put(
            f"/todos/{todo_id_to_update}",
            json={"done": new_done_status},
            name="/todos/{id} (PUT)"
        )

    # Note: A DELETE task is omitted to prevent the test from failing
    # as it runs. If you delete items 1 or 2, the 'get_single_todo'
    # and 'update_todo' tasks would start returning 404 errors.
    # For a more complex test, you could have an 'on_start'
    # method to seed data and a 'safe' delete task that only
    # deletes items it created.

    @task(1)
    def delete_todo(self):
        
        if self.created_todo_ids:
            
            todo_id_to_delete = random.choice(self.created_todo_ids)
            
            
            response = self.client.delete(
                f"/todos/{todo_id_to_delete}",
                name="/todos/{id} (DELETE)"
            )
            
            
            if response.status_code in [200, 204]:
                self.created_todo_ids.remove(todo_id_to_delete)
        else:
            
            pass 

    @task(1)
    def get_root(self):
        """
        Simulates a user hitting the welcome page.
        """
        self.client.get("/", name="/ (GET)")

    
    
