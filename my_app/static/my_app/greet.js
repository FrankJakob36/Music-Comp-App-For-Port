let composition = [];

function playAudio(note) {
    const audio = new Audio(`/static/player/sounds/${note}.mp3`);
    audio.play().catch(error => {
        console.error(`Error playing note ${note}:`, error);
        alert('Could not play sound. Please check your files and try again.');
    });
}

function addNoteAndPlay(note) {
    composition.push(note);
    updateCompositionDisplay();
    playAudio(note);
}

function playComposition() {
    if (composition.length === 0) {
        alert('No notes in the composition!');
        return;
    }
    composition.forEach((note, index) => {
        setTimeout(() => {
            playAudio(note);
        }, index * 600); // 600ms between notes for better timing
    });
}

function saveComposition() {
    fetch('/save/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ composition: composition })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Composition saved successfully!');
        } else {
            alert('Error saving composition: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred while saving.');
    });
}

function newComposition() {
    composition = [];
    updateCompositionDisplay();
}

function updateCompositionDisplay() {
    const compositionDiv = document.getElementById('composition');
    if (composition.length === 0) {
        compositionDiv.innerText = 'Current Composition: None';
    } else {
        compositionDiv.innerText = `Current Composition: ${composition.join(' - ')}`;
    }
}

function getCSRFToken() {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : '';
}
