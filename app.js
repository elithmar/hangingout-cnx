let mockEvents = [];
let currentFilter = 'All';

function fetchEvents() {
    mockEvents = window.eventsData || [];
    renderEvents();
}

function renderEvents() {
    const feed = document.getElementById('event-feed');
    feed.innerHTML = ''; // Clear existing

    // Filtrar los eventos seg√∫n la pesta√±a seleccionada
    const filteredEvents = currentFilter === 'All' 
        ? mockEvents 
        : mockEvents.filter(event => {
            // Comparamos el texto del filtro con la categor√≠a o tipo
            const filterText = currentFilter.toLowerCase();
            return event.category.toLowerCase().includes(filterText) || 
                   event.type.toLowerCase().includes(filterText) ||
                   (filterText === 'live music' && event.type === 'music') ||
                   (filterText === 'art' && event.type === 'culture');
        });

    if (filteredEvents.length === 0) {
        feed.innerHTML = '<div style="text-align:center; padding:40px; color:var(--text-muted);">No hay eventos de este tipo hoy.</div>';
        return;
    }

    filteredEvents.forEach(event => {
        const card = document.createElement('div');
        card.className = `event-card ${event.type}`;
        
        card.innerHTML = `
            <img src="${event.imageUrl}" alt="${event.title}" class="event-image">
            <div class="event-details">
                <div class="event-time">${event.time}</div>
                <div class="event-title">
                    ${event.title}
                    <span class="free-tag">FREE</span>
                </div>
                <div class="event-venue">${event.venue}</div>
                <div class="event-meta">
                    <span class="event-category">${event.category} | ${event.timeStatus}</span>
                    <span>${event.attending} Attending</span>
                </div>
            </div>
        `;
        
        feed.appendChild(card);
    });
}

// Set current date in header
function setDateHeader() {
    const dateHeader = document.getElementById('current-date');
    const options = { weekday: 'short', day: 'numeric', month: 'short' };
    const dateString = new Date().toLocaleDateString('en-US', options).toUpperCase();
}

// Filter interaction
function initFilters() {
    const chips = document.querySelectorAll('.filter-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            // Remove active class from all
            chips.forEach(c => c.classList.remove('active'));
            // Add to clicked
            chip.classList.add('active');
            
            // Actualizar filtro y re-renderizar
            currentFilter = chip.innerText;
            
            const feed = document.getElementById('event-feed');
            feed.style.opacity = '0.5';
            setTimeout(() => {
                renderEvents();
                feed.style.opacity = '1';
            }, 300);
        });
    });
}

// Bottom nav interaction
function initNav() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setDateHeader();
    fetchEvents();
    initFilters();
    initNav();
});
