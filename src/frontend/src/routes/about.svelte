<script>
import * as test_dict from './_tests/json-test.json'
</script>

<main>
	<div class="flex justify-center">
	    <div class="w-[100vw] xl:w-[40vw]">
	        <div class="flex items-center my-4 before:flex-1 before:border-t before:border-gray-300 before:mt-0.5 after:flex-1 after:border-t after:border-gray-300 after:mt-0.5">
	            <p class="text-center font-semibold text-xl mx-4 mb-0 dark:text-white">
	            Deep Philosophical Questions
	            </p>
	        </div>
	    </div>
	</div>
	<div class="pointless_ramble">
		<p>Some people ask <i>"why"</i>? Others may ask <i>"who"</i>? But the real question, as posed by the great Anderssen is the unspoken <i>"Are you sure you want to capture that?</i>".</p>
		<p>We, however, pose the question: "<i>Ipsum</i>"". It's not a <i>real</i> question. It's rhetorical. And it deserves the rhetorical answer: "<i>Lorem</i>". So Lorem Ipsum, dolor sit amet. Lorem all the Ipsum.</p>
	</div>
	<div class="flex justify-center mt-30">
	    <div class="lg:w-[40vw]">
	        <div class="flex items-center my-4 before:flex-1 before:border-t before:border-gray-300 before:mt-0.5 after:flex-1 after:border-t after:border-gray-300 after:mt-0.5">
	            <p class="text-center font-semibold text-xl mx-4 mb-0 dark:text-white">
	            I'll Try to Take this Seriously
	            </p>
	        </div>
	    </div>
	</div>
	<div class="pointless_ramble">
		<figure>
			<img src='/about_office.jpg' alt='Stock photo of an office environment. A person is pointing to a laptop screen at what appears to be Russia. Greenland and Brazil are inexplicably highlighted as places of interest. There is no deep meaning in this photo.'/>
			<figcaption>Photo by fauxels from Pexels. CC0.</figcaption>
		</figure>
		<p>I seriously have the design skills of a preschooler and there is no fingerpaint. You're also missing out on a great origin story with a heap of stock photos because I'm now sleepy. I also have concerns about {test_dict.concerns} when I do stuff like this.</p>
		<br>
		<p>You wanna see some json dumps?</p>
		<p>Here are some rankings:</p>
		<p>1st - {test_dict.Rankings.first}.</p>
		<p>2nd - {test_dict.Rankings.second}.</p>
		<p>3rd - {test_dict.Rankings.third}.</p>
	</div>
</main>

<style>
	.pointless_ramble {
		margin: 2em;
		padding: .1em;
	}
	.pointless_ramble p {
		margin: 1rem;
		letter-spacing: 0.065rem;
		word-spacing: 0.08rem;
		line-height: 1.7;
	}
	.pointless_ramble figure {
		font-size: smaller;
		height: 400px;
		width: 300px;
		object-fit: cover;
		float: left;
		padding: 1rem;
	}

</style>
