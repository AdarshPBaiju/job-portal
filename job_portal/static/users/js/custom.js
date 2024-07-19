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
    setupSearchInput('id_interests', 'Search interests');
    setupSearchInput('id_hobbies', 'Search hobbies');
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

        skillSelect.parentNode.insertBefore(skillSearchInput, skillSelect);

        const originalOptions = Array.from(skillSelect.options);

        function filterOptions(searchText) {
            skillSelect.innerHTML = '';
            originalOptions.forEach(function(option) {
                const optionText = option.textContent.toLowerCase();
                if (optionText.startsWith(searchText.toLowerCase())) {
                    skillSelect.appendChild(option.cloneNode(true));
                }
            });
        }

        skillSearchInput.addEventListener("input", function() {
            const searchText = skillSearchInput.value.trim();
            filterOptions(searchText);
        });

        filterOptions('');
    }
});


// Pause video
document.addEventListener('DOMContentLoaded', function () {
    var player = document.getElementById('player');
    var modal = document.getElementById('shortReelModal');
    var closeModalBtn = modal ? modal.querySelector('.btn-close-custom') : null;

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            if (player && !player.paused) {
                player.pause();
            }
        });
    }
});


// Select Job Profile Type
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('jobseekerLink')) {
        document.getElementById('jobseekerLink').addEventListener('click', function(e) {
            e.preventDefault();
            if (!document.getElementById('jobseekerRadio').checked) {
                document.getElementById('jobseekerRadio').checked = true;
                toggleButtonStyle('jobseekerLink');
                deselectOther('employerLink');
            }
        });
    }

    if (document.getElementById('employerLink')) {
        document.getElementById('employerLink').addEventListener('click', function(e) {
            e.preventDefault();
            if (!document.getElementById('employerRadio').checked) {
                document.getElementById('employerRadio').checked = true;
                toggleButtonStyle('employerLink');
                deselectOther('jobseekerLink');
            }
        });
    }

    if (document.getElementById('continueBtn')) {
        document.getElementById('continueBtn').addEventListener('click', function() {
            var selectedType = document.querySelector('input[name="type"]:checked');
            if (selectedType) {
                document.getElementById('profileForm').submit();
            } else {
                alert('Please select a profile type.');
            }
        });
    }
});

function toggleButtonStyle(linkId) {
    var link = document.getElementById(linkId);
    if (link.classList.contains('btn-outline-custom')) {
        link.classList.remove('btn-outline-custom');
        link.classList.add('btn-custom');
    } else {
        link.classList.remove('btn-custom');
        link.classList.add('btn-outline-custom');
    }
}

function deselectOther(otherLinkId) {
    var otherLink = document.getElementById(otherLinkId);
    if (otherLink.classList.contains('btn-custom')) {
        otherLink.classList.remove('btn-custom');
        otherLink.classList.add('btn-outline-custom');
    }
}


// Multiple Image input field add class form-control
document.addEventListener('DOMContentLoaded', function() {
    var imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.classList.add('form-control');
    }
});



// video player
document.addEventListener('DOMContentLoaded', function() {
    var video = document.getElementById('player');
    var playpauseBtn = document.getElementById('playpause-btn');
    var volumeBar = document.getElementById('volume-bar');
    var progressBar = document.getElementById('progress-bar');
    var progressContainer = document.getElementById('progress-container');
    var backwardBtn = document.getElementById('backward-btn');
    var forwardBtn = document.getElementById('forward-btn');
    var currentTimeDisplay = document.getElementById('current-time');
    var totalDurationDisplay = document.getElementById('total-duration');
    var isDragging = false;

    // Function to safely add event listeners
    function addListener(element, event, handler) {
        if (element) {
            element.addEventListener(event, handler);
        }
    }

    if (video) {
        video.addEventListener('loadedmetadata', function() {
            // Set initial volume and progress bar width
            if (volumeBar) {
                volumeBar.value = video.volume;
            }
            if (progressBar) {
                progressBar.style.width = '0%';
            }

            // Display total duration
            if (totalDurationDisplay) {
                var totalDuration = formatTime(video.duration);
                totalDurationDisplay.textContent = totalDuration;
            }
        });

        video.addEventListener('timeupdate', function() {
            if (!isDragging && progressBar) {
                var percent = (video.currentTime / video.duration) * 100;
                progressBar.style.width = percent + '%';
            }

            // Display current time
            if (currentTimeDisplay) {
                var currentTime = formatTime(video.currentTime);
                currentTimeDisplay.textContent = currentTime;
            }
        });

        video.addEventListener('ended', function() {
            if (playpauseBtn) {
                playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-play"></i>';
            }
        });
    }

    addListener(playpauseBtn, 'click', function() {
        if (video.paused || video.ended) {
            video.play();
            playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-pause"></i>';
        } else {
            video.pause();
            playpauseBtn.innerHTML = '<i class="fa-regular fa-circle-play"></i>';
        }
    });

    addListener(volumeBar, 'input', function() {
        video.volume = volumeBar.value;
    });

    addListener(backwardBtn, 'click', function() {
        video.currentTime -= 10; // Jump backward 10 seconds
    });

    addListener(forwardBtn, 'click', function() {
        video.currentTime += 10; // Jump forward 10 seconds
    });

    addListener(progressContainer, 'mousedown', function(e) {
        isDragging = true;
        seek(e);
    });

    addListener(document, 'mousemove', function(e) {
        if (isDragging) {
            seek(e);
            if (progressContainer && currentTimeDisplay) {
                var rect = progressContainer.getBoundingClientRect();
                var offsetX = e.clientX - rect.left;
                var percent = Math.max(0, Math.min(1, offsetX / rect.width));
                var newTime = percent * video.duration;
                currentTimeDisplay.textContent = formatTime(newTime);
            }
        }
    });

    addListener(document, 'mouseup', function(e) {
        if (isDragging) {
            isDragging = false;
            seek(e);
        }
    });

    function seek(e) {
        if (progressContainer && progressBar) {
            var rect = progressContainer.getBoundingClientRect();
            var offsetX = e.clientX - rect.left;
            var percent = Math.max(0, Math.min(1, offsetX / rect.width));
            video.currentTime = percent * video.duration;
            progressBar.style.width = percent * 100 + '%';
        }
    }

    function formatTime(seconds) {
        var minutes = Math.floor(seconds / 60);
        var secs = Math.floor(seconds % 60);
        var millis = Math.floor((seconds % 1) * 1000);
        return (minutes < 10 ? '0' : '') + minutes + ':' + 
               (secs < 10 ? '0' : '') + secs + ':' + 
               (millis < 100 ? '0' : '') + (millis < 10 ? '0' : '') + millis;
    }
});

// Notification Count and mark as read
document.addEventListener('DOMContentLoaded', function() {
    function updateNotificationCount() {
        fetch(notificationcountUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('notificationCount').textContent = data.unread_count;
        })
    }

    document.getElementById('notificationButton').addEventListener('click', function() {
        fetch(notificationcountUrl, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            updateNotificationCount();
        })
    });

    // Initialize notification count on page load
    updateNotificationCount();

    // Auto-reload notification count every 30 seconds
    setInterval(updateNotificationCount, 10000); // 30000 milliseconds = 30 seconds
});


// Load Notification
$(document).ready(function() {
    function loadNotifications() {
        $.ajax({
            url: notificationsUrl,
            method: 'GET',
            success: function(data) {
                data.sort(function(a, b) {
                    return new Date(b.created) - new Date(a.created);
                });
                let notificationsHtml = '';
                data.forEach(notification => {
                    notificationsHtml += `
                        <a href="${notification.url}" class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">
                            <img src="${notificationImage}" alt="notification" width="32" height="32" class="flex-shrink-0">
                            <div class="d-flex gap-2 w-100 justify-content-between">
                                <div>
                                    <h6 class="mb-0">${notification.subject}</h6>
                                    <p class="mb-0 opacity-75">${notification.content}</p>
                                </div>
                                <small class="opacity-50 text-nowrap">${moment(notification.created).fromNow()}</small>
                            </div>
                        </a>
                    `;
                });
                $('#notificationList').html(notificationsHtml);
            },
        });
    }

    $('#notificationModal').on('show.bs.modal', function () {
        loadNotifications();
    });
});
