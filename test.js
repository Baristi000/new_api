const data = ["sdsd", "sdsd"];
const fetch = require("node-fetch");
fetch('http://localhost:8000/url/add-new-url', {
  method: 'POST', // or 'PUT'
  headers: {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaWQiOjEsInNjb3BlcyI6WyJtZSIsInJlYWRfdXNlciIsInJlYWRfc2hvcCIsInJlYWRfY2hhbm5lbCIsInJlYWRfY291bnRyeSIsInJlYWRfc2ltIiwiY2hhbm5lbF9tYW5hZ2VyIiwic2hvcF9leGVjdXRvciIsInNob3Bfc2ltIiwiaW5hY3RpdmF0ZV91c2VyIiwidXJsIl0sImV4cCI6MTYwMjgwMTg1NH0.xZ__ANt1JjPHhbPB1UBxVV299_3ljYE-7Ca7YPSbe2c',
  },
  body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => {
  console.log('Success:', data);
})
.catch((error) => {
  console.error('Error:', error);
});
