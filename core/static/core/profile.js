document.addEventListener('DOMContentLoaded', function() {
	console.log('done')
		
	var profile = JSON.parse(document.querySelector('#profile').textContent)
	var user_id = JSON.parse(document.querySelector('#user_id').textContent)

	console.log(user_id)
	
	document.querySelector("#background-form").addEventListener("change", (e) => profileChange(e, "background", profile, user_id))
	
	document.querySelector("#family-history-form").addEventListener("change", (e) => profileChange(e, "family_history", profile, user_id))
	
	document.querySelector("#general-form").addEventListener("change", (e) => profileChange(e, "general", profile, user_id))
	
})

function profileChange(e, category, profile, user_id) {
	profile[category][e.target.name] = e.target.value
	
	fetch('/api/profile/'+user_id+'/', {
		method: 'PATCH',
		credentials: "include",
		headers: {
			"X-CSRFToken": getCookie("csrftoken"),
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Cache': 'no-cache'
		},
		body: JSON.stringify({
			"profile": profile
		}),
	})
	.then(response => {
		console.log('updated')
	})
	.catch(err => {
		console.log(err)
	})
}

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}