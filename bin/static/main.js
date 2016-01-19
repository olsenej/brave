var client = new ZeroClipboard( document.getElementById("copy_button") );

client.on( "ready", function( readyEvent ) {
// alert( "ZeroClipboard SWF is ready!" );
 
	client.on( 'copy', function(event) {
		event.clipboardData.setData('text/plain', event.target.value);
	} );
 
	client.on( "aftercopy", function( event ) {
		event.target.style.background = "green";
		event.target.innerHTML = "Copied!";
	} );
} );
