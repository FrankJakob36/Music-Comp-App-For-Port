let composition = [];

// Function to play a single note
function playAudio(note) {
    const audio = new Audio(`/static/player/sounds/${note}.mp3`);
    audio.play().catch(error => {
        console.error(`Error playing note ${note}:`, error);
        alert('Could not play sound. Please check your files and try again.');
    });
}

// Function to add a note and immediately play it
function addNoteAndPlay(note) {
    composition.push(note);
    updateCompositionDisplay();
    playAudio(note);
}

// Function to play the entire composition (sequence of notes)
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

// Function to save the composition (you can use it later if needed)

// Function to reset (clear) the current composition
function newComposition() {
    composition = [];
    updateCompositionDisplay();
}

// Function to update the display of the current composition
function updateCompositionDisplay() {
    const compositionDiv = document.getElementById('composition');
    if (composition.length === 0) {
        compositionDiv.innerText = 'Current Composition: None';
    } else {
        compositionDiv.innerText = `Current Composition: ${composition.join(' - ')}`;
    }
}

// Helper function to get the CSRF token for AJAX requests
function getCSRFToken() {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : '';
}

// Bind the play button to the playComposition function
document.getElementById('play-button').addEventListener('click', playComposition);
