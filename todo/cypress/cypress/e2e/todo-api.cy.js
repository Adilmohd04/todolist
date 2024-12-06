describe('Todo API End-to-End Tests', () => {
    const username = 'adil';
    const password = '0004';
    const authHeader = `Basic ${btoa(username + ':' + password)}`;
  
    let taskId;
  
    it('should create a new todo item', () => {
      cy.request({
        method: 'POST',
        url: 'http://127.0.0.1:8000/tasks/', 
        headers: {
          'Authorization': authHeader, 
          'Content-Type': 'application/json'
        },
        body: {
          title: "Complete the assignment", 
          description: "Update with new details", 
          due_date: "2024-12-12", 
          tags: ["updated", "django"],
          status: "WORKING" 
        }
      }).then((response) => {
        expect(response.status).to.eq(201); 
        taskId = response.body.id; 
        expect(taskId).to.exist; 
        cy.screenshot('todo-create-success'); 
      });
    });
  
    it('should retrieve all todo items', () => {
      cy.request({
        method: 'GET',
        url: 'http://127.0.0.1:8000/tasks/', 
        headers: {
          'Authorization': authHeader 
        }
      }).then((response) => {
        expect(response.status).to.eq(200); 
        expect(response.body).to.be.an('array');
        cy.screenshot('todo-retrieve-all-success'); 
      });
    });
  
    it('should update the todo item', () => {
      expect(taskId).to.exist;
      cy.request({
        method: 'PUT',
        url: `http://127.0.0.1:8000/tasks/${taskId}/`, 
        headers: {
          'Authorization': authHeader, 
          'Content-Type': 'application/json'
        },
        body: {
          title: 'Updated Todo',
          description: 'Updated description',
          due_date: "2024-12-12", 
          tags: ["good", "good"], 
          status: "COMPLETED",
          completed: true
        }
      }).then((response) => {
        expect(response.status).to.eq(200); 
        expect(response.body.title).to.eq('Updated Todo');
        cy.screenshot('todo-update-success'); 
      });
    });
  
    it('should delete the todo item', () => {
      expect(taskId).to.exist; 
      cy.request({
        method: 'DELETE',
        url: `http://127.0.0.1:8000/tasks/${taskId}/`,
        headers: {
          'Authorization': authHeader
        }
      }).then((response) => {
        expect(response.status).to.eq(204); 
        cy.screenshot('todo-delete-success'); 
      });
    });
  
    it('should verify the deleted todo item no longer exists', () => {
      expect(taskId).to.exist;
      cy.request({
        method: 'GET',
        url: `http://127.0.0.1:8000/tasks/${taskId}/`, 
        failOnStatusCode: false, 
        headers: {
          'Authorization': authHeader 
        }
      }).then((response) => {
        expect(response.status).to.eq(404); 
        cy.screenshot('todo-deleted-verification'); 
      });
    });
  
  });