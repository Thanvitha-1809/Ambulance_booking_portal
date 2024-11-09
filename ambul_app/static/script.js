function getSuggestions() {
    const disease = document.getElementById('disease').value;

    // Fetch suggestions based on disease from the backend
    fetch(`/suggestions?disease=${disease}`)
        .then(response => response.json())
        .then(data => {
            const suggestionsDiv = document.getElementById('suggestionsResult');
            suggestionsDiv.innerHTML = `<h3>Suggestions for ${disease}</h3>`;
            
            // Check if there are any hospitals suggested
            if (data.suggestions.length === 0) {
                suggestionsDiv.innerHTML += `<p>No hospitals found for ${disease}</p>`;
            } else {
                // Display list of suggested hospitals
                const list = document.createElement('ul');
                data.suggestions.forEach(hospital => {
                    const listItem = document.createElement('li');
                    listItem.textContent = hospital;
                    list.appendChild(listItem);
                });
                suggestionsDiv.appendChild(list);
            }
        })
        .catch(error => console.error('Error:', error));
}
