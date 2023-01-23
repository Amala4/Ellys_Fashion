
$(document).ready(function() {
    
    //Run all the functions
    addToWishlist()
    addToCart()
    sumPrices()
    removeFromCart()
    placeOrder()
    removeFromWishlist()

    //product-filter
    $('#apply-filter').click(function(event) {

        var filterUrl = $(this).attr("data-url") ;
        var colourChoices = [];
        var sizeChoices = [];
        var minPrice = $("#minamount").val();
        var maxPrice = $("#maxamount").val();
        var kidsCategChoices = [];
        var menCategChoices = [];
        var womenCategChoices = [];
        

        //Get selected colours
        $('.colourChoice:checkbox:checked').each(function(){
            colourChoices.push($(this).val());
            });

        //Get selected sizes
        $('.sizeChoice:checkbox:checked').each(function(){
            sizeChoices.push($(this).val());
            });


        $.ajax({
            'method': 'GET',  
            'url': filterUrl,
            'data': {"colour": colourChoices,
                    "sizes": sizeChoices,
                    "minPrice": minPrice,
                    "maxPrice": maxPrice,
                    "kidsCat": kidsCategChoices,
                    "menCat": menCategChoices,
                    "womenCat": womenCategChoices,
                    },  
            success: function(dataReturned) {
                $('#product-list-template').replaceWith(dataReturned);
                    handlePageNumbers();
            }
        });

        function handlePageNumbers() {
            $('#pageprev').hide()
            $('#pagenext').hide()
            $('.cuspagenum').click(function(event) {
                        event.preventDefault();
                        pagenum= $(this).text()

                        $.ajax({
                            'method': 'GET',  
                            'url': filterUrl,
                            'data': {"colour": colourChoices,
                                    "sizes": sizeChoices,
                                    "minPrice": minPrice,
                                    "maxPrice": maxPrice,
                                    "kidsCat": kidsCategChoices,
                                    "menCat": menCategChoices,
                                    "womenCat": womenCategChoices,
                                    "pagenum": pagenum,
                                    },
                            success: function(dataReturned) {
                                $('#product-list-template').replaceWith(dataReturned);
                                handlePageNumbers();
                            }
                        });
                    });
            addToWishlist()
            addToCart()
            
        }
    });

    //runs when qty is increased in cart
    $('.cart__totalprice').on("newTotal", function(e) {
        sumPrices()
    });

  

    function addToWishlist(){
        $('.wishlist').click(function(event) {
            var product_id = $(this).attr("p_id") ;
            var wishlistUrl = $(this).attr("data-url") ;
    
            $.ajax({
                'method': 'GET',  
                'url': wishlistUrl,
                'data': {"product_id": product_id,
                        "addToWish": "addToWish",
                        },  
                success: function(dataReturned) {
                    var statusRepsonse = dataReturned['saved']
                    if (statusRepsonse == 'True'){
                        $('.wishlist_count').text(dataReturned['wishlist_count']);
                        $('.wishlist_count_mobile').text(dataReturned['wishlist_count']);
                        alert("Your wishlist has been Saved");
                        }
                    else{
                        alert("Please login to save to wishlist");
                    }
                  
                }
            });
    
            
        });
    }
    


    function addToCart(){
        $('.a_cart').click(function(event) {
            var product_id = $(this).attr("p_id") ;
            var product_price = $(this).attr("p_price") ;
            var product_name = $(this).attr("p_name") ;
            var imageUrl = $(this).attr("p_imgurl") ;
            var cartUrl = $(this).attr("data-url") ;
            
            //checks if request is coming from add to cart in product detail
            if($('#qtypro').length){
                var quantity = $('#qtypro').val();
                var product_price_tot = parseFloat(product_price)*parseFloat(quantity);

            }
            else{
                var quantity = $(this).attr("qty") ;
                var product_price_tot = product_price
            }


            $.ajax({
                'method': 'GET',  
                'url': cartUrl,
                'data': {"product_id": product_id,
                        "product_price": product_price,
                        "quantity": quantity,
                        "product_price_tot": product_price_tot,
                        "addToCart": "addToCart",
                        "product_name": product_name,
                        "imageUrl": imageUrl,
                        },  
                success: function(dataReturned) {
                    var statusRepsonse = dataReturned['added']
                    if (statusRepsonse == 'True'){ 

                            $('.cart_count').text(dataReturned['count']);
                            $('.cart_count_mobile').text(dataReturned['count']);
                    }
                }
            });
    
            
        });
    }
    

    //produces the total price in cart
    function sumPrices(){
        var totalPrice_arr = [];
        var deliveryFee = $('#cart__delivery_fee ').text().replace(/[^\d]+/g,'');

        $( '.cart__totalspan' ).each(function( index, value ) {
            totalPrice_arr.push($(this).text().replace(/[^\d]+/g,''));
      });

        subtotal = 0;
        
        $.each(totalPrice_arr,function(){
            subtotal+=parseFloat(this) || 0;
        });

        total = parseFloat(deliveryFee)+subtotal;
        $("#cart__subtotalprice").text("₦ "+subtotal.toLocaleString('en-US'));
        $("#cart__totalprice").text("₦ "+total.toLocaleString('en-US'));

    }



    function removeFromCart(){
        $('.icon_close').click(function() {
            var currentRow = $(this).closest("tr");
            var product_id = currentRow.find('.cartpro_id').html();
            var cartUrl = $(this).attr("data-url") ;


            $.ajax({
                'method': 'GET',  
                'url': cartUrl,
                'data': {"product_id": product_id,
                        "remFroCart": "remFroCart",
                        },  
                success: function(dataReturned) {
                    var statusRepsonse = dataReturned['removed']
                    if (statusRepsonse == 'True'){
                        $('.cart_count').text(dataReturned['count']);
                        $('.cart_count_mobile').text(dataReturned['count']);
                        currentRow.remove();
                        sumPrices()
                    }
                }
            });
        });
    }



    function placeOrder(){
        $('#ordProceed').click(function(event) {
            
            var order_ids = [];
            var order_prices = [];
            var order_qtys = [];
            var phoneNo = document.getElementById("ordPhnNo").value;
            var address = document.getElementById("ordDelAddr").value;
            var orderTot = $('#cart__totalprice ').text();
            var cartUrl = $(this).attr("data-url") ;
            var loginUrl = $(this).attr("login-url") ;
            var isloggedin = $(this).attr("login-status") ;

            if(isloggedin == 'False'){
                window.location.href = loginUrl;
                return false;
            }
            

            if ($("#cartTable > tbody").children().length == 0)
            { 
                alert("Cart is empty");  	
                return false; 
            }

            if (phoneNo.length == 0)
            { 
                alert("Please add your phone number");  	
                return false; 
            }  	

            if (address.length == 0)
            { 
                alert("Please add your delivery address");  	
                return false; 
            }
                
            // loop over each table row 
            $("#cartTable tr").each(function(index){
                var currentRow=$(this);
                
                if (index !== 0) {

                    var product_id = currentRow.find('.cartpro_id').html();
                    var priceTot=currentRow.find("td:eq(3)").text();
                    var qty=currentRow.find('.cart__qty').html();
                    
                    order_ids.push(product_id);
                    order_prices.push(priceTot);
                    order_qtys.push(qty);
                 }
                
            });


            $.ajax({
                'method': 'GET',  
                'url': cartUrl,
                'data': {"order_ids": order_ids,
                        "order_prices": order_prices,
                        "order_qtys": order_qtys,
                        "placeOrder": "placeOrder",
                        "phoneNo": String(phoneNo),
                        "address": address,
                        "orderTot": orderTot,
                        },  
                success: function(dataReturned) {
                    $("#cartTable tr").each(function(){
                        $(this).remove()
                    });
                    $('.cart_count').text(0);
                    $('.cart_count_mobile').text(0);
                    $("#ordPhnNo").val("");
                    $("#ordDelAddr").val("");
                    sumPrices()
                    $('#alertResponse').replaceWith(dataReturned);
                }
            });
        });

    }



    function removeFromWishlist(){
        $('.wishlist_remove').click(function() {
            var currentRow = $(this).closest("tr");
            var product_id = currentRow.find('.wishpro_id').html();
            var wishlistUrl = $(this).attr("data-url") ;


            $.ajax({
                'method': 'GET',  
                'url': wishlistUrl,
                'data': {"product_id": product_id,
                        "remFroWish": "remFroWish",
                        },  
                success: function(dataReturned) {
                    var statusRepsonse = dataReturned['removed']
                    if (statusRepsonse == 'True'){
                        currentRow.remove();
                        $('.wishlist_count').text(dataReturned['wishlist_count']);
                        $('.wishlist_count_mobile').text(dataReturned['wishlist_count']);
                        alert("Item removed from wishlist")
                        
                    }
                }
            });
        });
    }
});
