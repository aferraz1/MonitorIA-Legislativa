// Main JavaScript for MonitorIA Legislativa

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Smooth scrolling
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if(target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });

    // Search functionality
    $('#searchForm').on('submit', function(e) {
        var searchQuery = $('#searchInput').val().trim();
        if (searchQuery === '') {
            e.preventDefault();
            alert('Por favor, digite algo para buscar.');
        }
    });

    // Confirm delete actions
    $('.delete-confirm').on('click', function(e) {
        if (!confirm('Tem certeza que deseja excluir este item?')) {
            e.preventDefault();
        }
    });

    // Auto-dismiss alerts after 5 seconds
    $('.alert').not('.alert-permanent').delay(5000).fadeOut('slow');

    // Loading overlay
    function showLoading() {
        $('body').append('<div class="spinner-overlay"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Carregando...</span></div></div>');
    }

    function hideLoading() {
        $('.spinner-overlay').remove();
    }

    // AJAX form submission example
    $('.ajax-form').on('submit', function(e) {
        e.preventDefault();
        showLoading();
        
        $.ajax({
            url: $(this).attr('action'),
            method: $(this).attr('method'),
            data: $(this).serialize(),
            success: function(response) {
                hideLoading();
                if (response.success) {
                    alert('Operação realizada com sucesso!');
                    location.reload();
                }
            },
            error: function() {
                hideLoading();
                alert('Erro ao processar requisição.');
            }
        });
    });

    // Dynamic filter updates
    $('.filter-select').on('change', function() {
        $(this).closest('form').submit();
    });

    // Copy to clipboard functionality
    $('.copy-btn').on('click', function() {
        var text = $(this).data('copy');
        navigator.clipboard.writeText(text).then(function() {
            alert('Copiado para a área de transferência!');
        });
    });

    // Print functionality
    $('.print-btn').on('click', function() {
        window.print();
    });

    // Share functionality
    $('.share-btn').on('click', function(e) {
        e.preventDefault();
        var url = $(this).data('url') || window.location.href;
        var title = $(this).data('title') || document.title;
        
        if (navigator.share) {
            navigator.share({
                title: title,
                url: url
            });
        } else {
            prompt('Copie o link:', url);
        }
    });
});

// Chart utilities (for use with Chart.js if needed)
function createBarChart(canvasId, labels, data, label) {
    var ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(13, 110, 253, 0.5)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createPieChart(canvasId, labels, data) {
    var ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(13, 110, 253, 0.8)',
                    'rgba(25, 135, 84, 0.8)',
                    'rgba(220, 53, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(13, 202, 240, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
