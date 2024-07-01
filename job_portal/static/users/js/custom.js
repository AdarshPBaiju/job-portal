// Automatically close alerts after 5 seconds
window.onload = function() {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '1';
            alert.classList.add('fadeInRight');
        }, 100);
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.classList.remove('fadeInRight');
            alert.classList.add('fadeOutRight');
            setTimeout(function() {
                alert.remove();
            }, 1000);
        }, 4000);
    });
};

// Pagination Js
let currentPage = document.querySelector('.page-item.active');

if (currentPage) {
    let currentPageNum = parseInt(currentPage.querySelector('a').innerText);
    let totalPages = document.querySelectorAll('#pagination .count-page').length;

    const pagesToShow = 2;

    let pages = document.querySelectorAll('#pagination .page-item');
    pages.forEach(page => page.style.display = 'none');

    let startPage;
    if (currentPageNum === 1) {
        startPage = 1;
    } else if (currentPageNum === 2) {
        startPage = 1;
    } else if (currentPageNum === totalPages) {
        startPage = Math.max(1, currentPageNum - 4);
    } else if (currentPageNum === totalPages - 1) {
        startPage = Math.max(1, currentPageNum - 3);
    } else {
        startPage = Math.max(1, currentPageNum - pagesToShow);
    }

    let endPage = Math.min(totalPages, startPage + 4);

    if (endPage - startPage + 1 < 5) {
        startPage = Math.max(1, endPage - 4);
    }

    for (let i = startPage; i <= endPage; i++) {
        let pageToShow = document.querySelector(`#pagination .page-item:nth-child(${i + 1})`);
        if (pageToShow) {
            pageToShow.style.display = 'block';
        }
    }

    document.getElementById('prevPage').style.display = 'block';
    document.getElementById('nextPage').style.display = 'block';

    if (currentPageNum === 1) {
        document.getElementById('prevPage').classList.add('disabled');
        document.getElementById('prevPage').querySelector('a').setAttribute('aria-disabled', 'true');
    } else {
        document.getElementById('prevPage').classList.remove('disabled');
        document.getElementById('prevPage').querySelector('a').removeAttribute('aria-disabled');
    }

    if (currentPageNum === totalPages) {
        document.getElementById('nextPage').classList.add('disabled');
        document.getElementById('nextPage').querySelector('a').setAttribute('aria-disabled', 'true');
    } else {
        document.getElementById('nextPage').classList.remove('disabled');
        document.getElementById('nextPage').querySelector('a').removeAttribute('aria-disabled');
    }
}


// Multi Select Search Box
document.addEventListener('DOMContentLoaded', function() {
    function setupSearchInput(selectId, placeholderText) {
        var selectElement = document.getElementById(selectId);
        if (!selectElement) return;

        var searchInput = document.createElement('input');
        searchInput.setAttribute('type', 'text');
        searchInput.setAttribute('class', 'form-control mb-2');
        searchInput.setAttribute('placeholder', placeholderText);

        var formGroup = selectElement.closest('.form-group');
        if (!formGroup) return;

        formGroup.insertBefore(searchInput, selectElement);

        searchInput.addEventListener('input', function() {
            var searchText = this.value.toLowerCase();
            var options = selectElement.querySelectorAll('option');

            options.forEach(function(option) {
                var optionText = option.textContent.toLowerCase();
                if (optionText.includes(searchText)) {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'none';
                }
            });
        });
    }

    // Usage without error messages
    setupSearchInput('id_interest', 'Search interests');
    setupSearchInput('id_hobby', 'Search hobbies');
});


// Skill Search
document.addEventListener("DOMContentLoaded", function() {
    const skillSelect = document.getElementById("id_skill");

    // Check if skillSelect exists
    if (skillSelect) {
        const skillSearchInput = document.createElement("input");
        skillSearchInput.type = "text";
        skillSearchInput.id = "skillSearch";
        skillSearchInput.classList.add("form-control");
        skillSearchInput.classList.add("mb-2");
        skillSearchInput.placeholder = "Search skill...";

        // Insert the search input before the select element
        skillSelect.parentNode.insertBefore(skillSearchInput, skillSelect);

        // Options array to store original options for reset
        const originalOptions = Array.from(skillSelect.options);

        // Function to filter options based on search text
        function filterOptions(searchText) {
            skillSelect.innerHTML = ''; // Clear all options
            originalOptions.forEach(function(option) {
                const optionText = option.textContent.toLowerCase();
                if (optionText.startsWith(searchText.toLowerCase())) {
                    skillSelect.appendChild(option.cloneNode(true)); // Append filtered options
                }
            });
        }

        // Event listener for filtering options based on search input
        skillSearchInput.addEventListener("input", function() {
            const searchText = skillSearchInput.value.trim(); // Trim whitespace
            filterOptions(searchText);
        });

        // Initial load: Show all options
        filterOptions('');
    }
});


// Pause video
document.addEventListener('DOMContentLoaded', function () {
    var player = document.getElementById('player');
    var modal = document.getElementById('shortReelModal');
    var closeModalBtn = modal ? modal.querySelector('.btn-close') : null;

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            if (player && !player.paused) {
                player.pause();
            }
        });
    }
});