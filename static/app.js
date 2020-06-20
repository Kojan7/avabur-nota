$(document).ready(function(){
	
	$('.updateButton').on('click', function() {
		var PrimaryBoots = $("bootsprimgem").val();
		var SecondaryBoots = $("bootssecgem").val();
		var PrimaryHelmet = $("helmetprimgem").val();
		var SecondaryHelmet = $("helmetsecgem").val();
		var PrimaryBreast = $("boobsprimgem").val();
		var SecondaryBreast = $("boobssecgem").val();
		var PrimaryGloves = $("glovesprimgem").val();
		var SecondaryGloves = $("glovessecgem").val();
		var PrimaryOffhand = $("shieldprimgem").val();
		var SecondaryOffhand = $("shieldsecgem").val();
		var PrimaryWeapon = $("weps_primgem").val();
		var SecondaryWeapon = $("weps_secgem").val();
		var TierIngr =$("select_tier").val();

		req = $.ajax({
			url : '/updateGemOrder',
			type : 'POST',
			data : {PrimaryBoots:PrimaryBoots, SecondaryBoots : SecondaryBoots, TierIngr : TierIngr }
		});

		req.done(function(){
			document.getElementById('resultstable').innerHTML = some_html
		})
		
	});
});