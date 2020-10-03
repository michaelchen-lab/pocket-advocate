document.addEventListener('DOMContentLoaded', function() {
	
	var my_symptoms = JSON.parse(document.querySelector('#my_symptoms').textContent)
	var records = JSON.parse(document.querySelector('#records').textContent)
	
	document.querySelector("#my_symptom").addEventListener("change", (e) => showSymptomGraph(e, my_symptoms, records))
	
	showSymptomGraph(event, my_symptoms, records)
})

function showSymptomGraph(e, my_symptoms, records) {
	e.preventDefault()
	
	const my_symptom_id = my_symptoms[document.querySelector("#my_symptom").value]
	console.log(my_symptom_id)
	console.log(my_symptoms)
	console.log(records)
	
	let labels = []
	let series = []
	records.forEach(record => {
		if (record.symptom_id === my_symptom_id) {
			labels.push(record.date)
			series.push(record.score)
		}
	})
	
	new Chartist.Line("#graph", {
		labels: labels,
		series: [series]
	}, {
		high: 10,
		low: 0,
	})
}