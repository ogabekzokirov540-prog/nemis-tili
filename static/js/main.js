// Filter lessons by category
function filterLessons(category) {
    const cards = document.querySelectorAll('.lesson-card');
    cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Search lessons
function searchLessons() {
    const searchInput = document.getElementById('searchBox');
    const filter = searchInput.value.toLowerCase();
    const cards = document.querySelectorAll('.lesson-card');
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(filter) || description.includes(filter)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Open lesson detail
function openLesson(lessonId) {
    fetch(`/api/lesson/${lessonId}`)
        .then(response => response.json())
        .then(data => {
            showLessonDetail(data);
        })
        .catch(error => console.error('Xatolik:', error));
}

// Show lesson detail modal
function showLessonDetail(lesson) {
    alert(`Dars: ${lesson.title}\nTur: ${lesson.category}\n\n${lesson.description}`);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Platform yuklandi');
});
