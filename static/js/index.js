var helpIcons = document.querySelectorAll(".help-icon");
var ctx = document.getElementById('featuresChart')?.getContext('2d');
var features = document.getElementById('featuresChart')?.getAttribute("data-features");

// Helper images popups
helpIcons.forEach(function(helpIcon) {
    var helpImage = helpIcon.parentElement.nextElementSibling;

    helpIcon.addEventListener("mouseover", function(event)
    {
        helpImage.style.display = "block";
    });

    helpIcon.addEventListener("mouseout", function(event)
    {
        helpImage.style.display = "none";
    });

    helpIcon.addEventListener("mousemove", function(event)
    {
        helpImage.style.top = event.clientY + "px";
        helpImage.style.left = event.clientX + "px";
    });
});

// If a response is available, parse it and plot the data
if(features != undefined)
{
    features = JSON.parse(features);

    var featuresChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(features),
            datasets: [{
                label: 'Features importance',
                data: Object.values(features),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}