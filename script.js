// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault();
    const text = document.getElementById('input').value;
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'text=' + encodeURIComponent(text)
    })
    .then(response => response.json())
    .then(data => {
        displayPassage(data.passage);
        displayQueries(data.queries);
    })
    .catch(error => console.log(error));
}

// Function to display retrieved passage
function displayPassage(passage) {
    const passageTextarea = document.getElementById('passage');
    passageTextarea.value = passage;
}

// Function to display generated queries
function displayQueries(queries) {
    const queriesTextarea = document.getElementById('queries');
    queriesTextarea.value = queries.slice(0, 5).join('\n');
}

// Add event listener to the form submit button
document.querySelector('form').addEventListener('submit', handleSubmit);
