let aliveSecond = 0;
let heartbeatRate = 1000;
let myChannel = "davidmccabe";
let pubnub;

//Rewrite using the fetch api

const setupPubNub = () =>{
    pubnub = new PubNub({
        publishKey: 'pub-c-0abc1efe-4b78-4cdc-a195-fc1ebc33eaac',
        subscribeKey: 'sub-c-6ed21369-a5b3-4a8b-b9a6-3a225ce51275',
        userId: "david"
    });

    const listener = {
        status: (statusEvent) => {
            if(statusEvent.category === "PNConnectedCategory"){
                console.log("Connected");
            }
        },
        message: (messageEvent) => {
            console.log(messageEvent);
        },
        presence: (presenceEvent) => {
            //Handle presence
        }
    };
    pubnub.addListener(listener);

    //subscribe to a channel
    pubnub.subscribe({channels: [myChannel]});
};
const publishMessage = async (message) => {
    const publishPayload = {
        channel : myChannel,
        message: {
            title: "Sensor values",
            description: message
        }
    };
    await pubnub.publish(publishPayload);
}
function keepAlive()
{
	fetch('/keep_alive')
	.then(response=>{
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error("Server offline")
	})
	.then(responseJson => {
		if(responseJson.motion == 1){
			document.getElementById("motion_id").innerHTML = "Motion Detected";
		}
		else
		{

			document.getElementById("motion_id").innerHTML = "No Motion Detected";
		}

		console.log(responseJson)})
	.catch(error => console.log(error));
	setTimeout('keepAlive()', heartbeatRate);
}

function live_video()
{
	fetch('/live_video')
	.then(response=>{
		if(response.ok){
			let date = new Date();
			aliveSecond = date.getTime();
			return response.json();
		}
		throw new Error("Camera offline")
	})
	.then(responseJson => {
		if(responseJson.motion == 1){
			document.getElementById("camera_id").innerHTML = "Camera is live";
		}
		else
		{

			document.getElementById("camera_id").innerHTML = "Camera is dead";
		}

		console.log(responseJson)})
	.catch(error => console.log(error));
	setTimeout('live_video()', heartbeatRate);
}
function time()
{
	let d = new Date();
	let currentSec = d.getTime();
	console.log(currentSec - aliveSecond)
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{

		document.getElementById("Connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("Connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}
function cameraTime()
{
	let d = new Date();
	let currentSec = d.getTime();
	console.log(currentSec - aliveSecond)
	if(currentSec - aliveSecond > heartbeatRate + 1000)
	{

		document.getElementById("camera_connection_id").innerHTML = "DEAD";
	}
	else
	{
		document.getElementById("camera_connection_id").innerHTML = "ALIVE";
	}
	setTimeout('time()', 1000);
}
function handleClick(cb){
	if(cb.checked){
		value = "ON";
	}else{
		value = "OFF";
	}
	publishMessage(cb.id+"-"+value);
}
function handleClick(cam){
	if(cam.checked){
		value = "ON";
	}else{
		value = "OFF";
	}
	publishMessage(cam.id+"-"+value);
}