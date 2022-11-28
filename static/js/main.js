let aliveSecond = 0;
let heartbeatRate = 5000;

//Rewrite using the fetch api
function keepAlive()
{
	fetch('/keep_alive')
	.then(response=> {
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error('Server offline');
	})
	.then(responseJson => console.log(responseJson))
	.catch(error => console.log(error));
	setTimeout('keepAlive()', heartbeatRate);
}

function time(){
	let d = new Date();
	let currentSec = d.getTime();
	if(currentSec - aliveSecond > heartbeatRate + 1000){
		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}