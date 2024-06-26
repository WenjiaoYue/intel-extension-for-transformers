<!--
  Copyright (c) 2024 Intel Corporation
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<script lang="ts">
	import { onDestroy } from "svelte";
	import { createEventDispatcher } from "svelte";
	import audioOff from "$lib/assets/voice/svg/voiceOff.svg";
    import voiceWave from '$lib/assets/voice/svg/voiceOn.svg'
	// Audio config

	const dispatch = createEventDispatcher()

	let chunks: any[] = [];
	let audioRecorder: MediaRecorder | undefined = undefined;
	let recordOK: boolean = false;
	let isRecording: boolean = false;
	let audioSrc: any = null;
	let interval: number;
    let voiceTimer = 0
	const MAX_AUDIO_TIME: number = 60;

	function pad(value: number) {
		return value.toString().padStart(2, "0");
	}

	function displayTimer(timer: number) {
		const minutes = pad(Math.floor(timer / 60));
		const seconds = pad(timer % 60);
		const time = `${minutes}:${seconds}`;
		return time;
	}

	async function getAudioPermission() {
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			await navigator.mediaDevices
				.getUserMedia({ audio: true })
				.then((stream) => {
					audioRecorder = new MediaRecorder(stream);

					audioRecorder.addEventListener("dataavailable", (event) => {
						chunks.push(event.data)
					});

					audioRecorder.addEventListener("stop", () => {
						if (voiceTimer < 10) {
							dispatch('fail')
						} else {
							const blob = new Blob(chunks, { type: "audio/mp3; codecs=opus" });
							audioSrc = window.URL.createObjectURL(blob);
							dispatch('done', {src: audioSrc})
						}
						chunks = []
						voiceTimer = 0;
					});
					recordOK = true;
				})
				.catch((error) => {
					console.error(`The following getUserMedia error occurred: ${error}`);
					recordOK = false;
				});
		} else {
			console.log("getUserMedia() is not supported in your browser");
			recordOK = false;
		}
	}

	async function toggleRecording() {
		if (!recordOK) {
			await getAudioPermission();
		}
		isRecording = !isRecording;
		if (isRecording) {
			console.log("Recording");
			audioRecorder?.start();
			interval = setInterval(updateTimer, 1000);
		} else {
			console.log("Stopped recording");
			audioRecorder?.stop();
			clearInterval(interval);
		}
	}

	function updateTimer() {
		if (voiceTimer++ >= MAX_AUDIO_TIME) {
			toggleRecording();
		}
	}

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<div class="relative w-full aspect-square flex flex-col justify-center items-center rounded-xl shadow-[0_2px_30px_0_rgba(0,0,0,0.1)] sm:w-[5rem] sm:h-[5rem] ">
	<!-- Voice button -->
	<span class="absolute -top-3 text-[#6578aa] text-sm">{displayTimer(voiceTimer)}</span>
	<label class="swap">
	
		<!-- this hidden checkbox controls the state -->
		<input type="checkbox" on:change={toggleRecording} class="hidden"/>
		
		<!-- volume on icon -->
		<img class="w-10 swap-on"
        class:hidden={!isRecording}
        src={voiceWave} alt=""/>
		<!-- <svg class="swap-on fill-current w-10 h-10" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 1024A512 512 0 1 1 512 0a512 512 0 0 1 0 1024z m3.008-92.992a416 416 0 1 0 0-832 416 416 0 0 0 0 832zM320 320h128v384H320V320z m256 0h128v384H576V320z" fill="#bcdbff"></path></svg> -->
		<!-- volume off icon -->
		<img class="w-10 swap-off " 
        class:hidden={isRecording}
        src={audioOff} alt="" />


		<!-- <svg class="swap-off fill-current w-10 h-10" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 1024A512 512 0 1 1 512 0a512 512 0 0 1 0 1024z m3.008-92.992a416 416 0 1 0 0-832 416 416 0 0 0 0 832zM383.232 287.616l384 224.896-384 223.104v-448z" fill="#bcdbff"></path></svg> -->
	</label>
	<span class="text-xs text-gray-500">{isRecording ? 'Recording' : 'Record'}</span>
	<!-- <span class="text-[#6578aa] text-xs">Limit: 00:10~01:00</span> -->
</div>
