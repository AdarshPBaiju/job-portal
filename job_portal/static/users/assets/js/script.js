document.addEventListener('DOMContentLoaded', function() {
    var alert = document.querySelector('.alert');
    setTimeout(function() {
        alert.classList.remove('slide-in');
        alert.classList.add('slide-out');
        setTimeout(function() {
            alert.remove();
        }, 500);
    }, 5000);
});