const data = ["sdsd", "sdsd"];

fetch('https://example.com/profile', {
  method: 'POST', // or 'PUT'
  headers: {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6ImFkbWluIiwiaWQiOjEsInNjb3BlcyI6WyJtZSIsInJlYWRfdXNlciIsInJlYWRfc2hvcCIsInJlYWRfY2hhbm5lbCIsInJlYWRfY291bnRyeSIsInJlYWRfc2ltIiwiY2hhbm5lbF9tYW5hZ2VyIiwic2hvcF9leGVjdXRvciIsInNob3Bfc2ltIiwiaW5hY3RpdmF0ZV91c2VyIiwidXJsIl0sImV4cCI6MTYwMjI5MzUzM30.6Lf7XuNWv1-6Qj8c4XyYpzeI-TyTTBqLFOpIt0uBqq8',
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
