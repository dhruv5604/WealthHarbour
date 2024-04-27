var renderChart=(data,labels)=>{
    var ctx =document.getElementById('myChart').getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [1,2,3,4,5,6,7,8,9,10],
            datasets: [{
                label: 'Networth',
                data: data,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor:[
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options:{
            scales:{
                yAxes:[{
                    ticks:{
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}


const getChartData=()=>{
    fetch("/networth/get_networth")
    .then(res=>res.json())
    .then((results)=>{
        console.log("results",results)
        const networth_data = results.networth_of_10_years;
        console.log("data",networth_data)
        const [labels,data]=[
            Object.keys(networth_data),
            Object.values(networth_data),
        ];

        renderChart(data,labels)
    })
}

document.onload= getChartData()