$(document).ready(function () {
    session = new QiSession("127.0.0.1:8002", "1.0");

    $('#page_accueil').show();
    $('#page_objet').hide();
    $('#page_rangement').hide();
    $('#page_en_cours').hide();


    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("PageAccueil").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_accueil').show();
                $('#page_objet').hide();
                $('#page_rangement').hide();
		        $('#page_en_cours').hide();
            });
        });


        ALMemory.subscriber("PageObjet").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_objet').show();
                $('#page_accueil').hide();
                $('#page_rangement').hide();
		        $('#page_en_cours').hide();
            });
        });

        ALMemory.subscriber("peluche").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_objet').show();
                $('#page_accueil').hide();
                $('#page_rangement').hide();
		        $('#page_en_cours').hide();
		        $('#button_peluche').hide();
		        $('#button_oiseau').show();
		        $('#button_ballon').show();
            });
        });



        ALMemory.subscriber("oiseau").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_objet').show();
                $('#page_accueil').hide();
                $('#page_rangement').hide();
		        $('#page_en_cours').hide();
		        $('#button_oiseau').hide();
		        $('#button_peluche').show();
		        $('#button_ballon').show();
            });
        });

        ALMemory.subscriber("ballon").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_objet').show();
                $('#page_accueil').hide();
                $('#page_rangement').hide();
		        $('#page_en_cours').hide();
		        $('#button_ballon').hide();
		        $('#button_peluche').show();
		        $('#button_oiseau').show();
            });
        });


        ALMemory.subscriber("PageRangement").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_rangement').show();
                $('#page_accueil').hide();
                $('#page_objet').hide();
		        $('#page_en_cours').hide();
            });
        });

        ALMemory.subscriber("carton").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_rangement').show();
                $('#page_accueil').hide();
                $('#page_objet').hide();
		        $('#page_en_cours').hide();
		        $('#button_carton').hide();
		        $('#button_fauteuil').show();
		        $('#button_table').show();
            });
        });

        ALMemory.subscriber("fauteuil").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_rangement').show();
                $('#page_accueil').hide();
                $('#page_objet').hide();
	            $('#page_en_cours').hide();
	            $('#button_fauteuil').hide();
		        $('#button_carton').show();
		        $('#button_table').show();
            });
        });

        ALMemory.subscriber("table").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_rangement').show();
                $('#page_accueil').hide();
                $('#page_objet').hide();
		        $('#page_en_cours').hide();
        	    $('#button_table').hide();
		        $('#button_fauteuil').show();
	            $('#button_carton').show();
            });
        });


        ALMemory.subscriber("PageEnCours").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_rangement').hide();
                $('#page_accueil').hide();
                $('#page_objet').hide();
		        $('#page_en_cours').show();
		
            });
        });

    });

    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }


    $('#ranger').on('click', function() {
        console.log("click Ranger");
        raise('ButtonRanger', 1)
    });


    $('#peluche').on('click', function() {
        console.log("click Peluche");
        raise('ButtonPeluche', 'peluche')
    });

    $('#oiseau').on('click', function() {
        console.log("click Oiseau");
        raise('ButtonOiseau', 'oiseau')
    });

    $('#ballon').on('click', function() {
        console.log("click Ballon");
        raise('ButtonBallon', 'ballon')
    });

    $('#carton').on('click', function() {
        console.log("click Carton");
        raise('ButtonCarton', 'carton')
    });

    $('#table').on('click', function() {
        console.log("click Table");
        raise('ButtonTable', 'table')
    });

    $('#fauteuil').on('click', function() {
        console.log("click Fauteuil");
        raise('ButtonFauteuil', 'fauteuil')
    });

    $('#new_object').on('click', function() {
        console.log("click Recommencer");
        raise('ButtonRecommencer', 1)
    });


});
