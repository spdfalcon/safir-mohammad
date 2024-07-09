document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('.home-search-input');
    const modal = document.querySelector('#myModal');

    // Function to open the modal
    function openModal() {
        modal.classList.add('modal-active');
    }

    // Add event listener to open modal when input field is clicked
    if (searchInput) {
        searchInput.addEventListener('click', function(event){
            event.preventDefault();
            openModal();
        });
    }

    // Function to toggle modal
    function toggleModal() {
        modal.classList.remove('modal-active');
    }

    // Close modal when overlay is clicked or close button is clicked
    const modalClose = document.querySelector('#modalClose');
    if (modalClose) {
        modalClose.addEventListener('click', toggleModal);
    }
    const modalOverlay = document.querySelector('.modal-overlay');

    if (modalOverlay) {
        modalOverlay.addEventListener('click', toggleModal);
    }
});

function updateTabContent(response) {
    // Function to generate HTML for search results
    function generateSearchResultsHTML(items) {
        return items.map(item => {
            // Check if the item has an image
            if (item.img) {
                return `<p class="pb-4">
                            <img class="item-thumbnail" src="${item.img}" alt="Thumbnail">
                            <a class="text-dark" href="${item.url}">${item.title}</a>
                        </p>`;
            } else {
                // Use the default icon path from the response
                return `<p class="pb-4">
                            <img class="item-thumbnail" src="${response.default_icon_path}" alt="Default Thumbnail">
                            <a class="text-dark" href="${item.url}">${item.title}</a>
                        </p>`;
            }
        }).join('');
    }
    
    

    // Update tab counts
    document.getElementById('packagesCount').innerText = "(" + response.packages_count + ")";
    document.getElementById('coursesCount').innerText = "(" + response.courses_count + ")";
    document.getElementById('partsCount').innerText = "(" + response.parts_count + ")";

    // Populate search results for each tab
    document.getElementById('searchResultsPackages').innerHTML = generateSearchResultsHTML(JSON.parse(response.packages));
    document.getElementById('searchResultsCourses').innerHTML = generateSearchResultsHTML(JSON.parse(response.courses));
    document.getElementById('searchResultsParts').innerHTML = generateSearchResultsHTML(JSON.parse(response.parts));
}

function performSearch(searchQuery) {
    if (searchQuery.trim() === '') {
        document.querySelector('#searchResults').style.display = 'none'; // Hide tabs if search query is empty
        return;
    }

    setTimeout(function() {
        document.querySelector('#searchResults').style.display = 'block'; // Show tabs with delay
    }, 500); // Adjust the delay time as needed

    var xhr = new XMLHttpRequest();
    var url = '/search_results_ajax/?search=' + encodeURIComponent(searchQuery);

  
    xhr.open('GET', url, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                updateTabContent(response); // Update tab content
                
            } else {
                console.error('Request failed: ' + xhr.status);
            }
        }
    };
    xhr.send();
}

function search() {
    var searchQuery = document.querySelector('.modal-search-input').value;
    performSearch(searchQuery);
}


function hideNonTabs() {
    console.log("Test")
    document.querySelectorAll('.nav-link').forEach(tab => {
        const tabId = tab.getAttribute('id');
        if (tabId !== 'packages-tab' && tabId !== 'courses-tab') {
            tab.style.display = 'none';
        }
    });
}

function showAllTabs() {
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.style.display = 'block'; // Show all tabs
    });
}


document.querySelector('.modal-search-input').addEventListener('keyup', search);

document.querySelectorAll('.search-button').forEach(button => {
    button.addEventListener('click', function(event) {
        // Prevent the default form submission behavior
        event.preventDefault();
        this.disabled = true;
    });
});

document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        // Prevent the default form submission behavior
        event.preventDefault();
    }
});

