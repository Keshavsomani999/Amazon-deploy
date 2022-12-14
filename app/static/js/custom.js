

function getItems(){
  db.collection("items").get().then((querySnapshot) => {
    let items = [];
    querySnapshot.forEach((doc) => {
        items.push({
          id: doc.id,
          image: doc.data().image,
          name: doc.data().name,
          make: doc.data().make,
          rating: doc.data().rating,
          price: doc.data().price
        })
    });
    generateItems(items);
});
}

function addToCart(item){
  console.log(item);
   let cartItem = db.collection("cart-items").doc(item.id);
   cartItem.get()
   .then(function(doc){
    if(doc.exists){
      cartItem.update({
        quantity:doc.data().quantity + 1 
      })
    } else {
      cartItem.set({
        image: item.image,
        name: item.name,
        make: item.make,
        rating: item.rating,
        price: item.price,
        quantity:1
      })
    }
   })
} 

function generateItems(items){
  let itemsHTML = "";
  items.forEach((item) => {
      let doc = document.createElement("div");
      doc.classList.add("main-product","mr-16");
      doc.innerHTML=`
      <div class="product-image w-48 h-52 bg-white rounded-lg flex justify-center items-center p-4">
      <img class="w-full object-contain" src="${item.image}">
        </div>
        <div class="product-name text-gray-700 font-bold mt-2 text-sm">
            ${item.name}
        </div>
        <div class="product.make text-green-700 font-bold">
        ${item.make}
        </div>
        <div class="product-rating text-yellow-300 font-bold my-1">
            ⭐⭐⭐⭐⭐ ${item.rating}
        </div>
        <div class="product-price text-gray-700 text-lg font-bold ">₹
        ${numeral(item.price).format('0,0.00')}
      `;

      let addToCartEl = document.createElement("div");
      addToCartEl.classList.add("hover:bg-yellow-600", "cursor-pointer", "product-add", "h-8", "w-28", "rounded", "bg-yellow-500", "text-white", "text-md", "flex", "justify-center", "items-center","mt-2");
      addToCartEl.innerText= "Add to cart";
      addToCartEl.addEventListener("click",function(){
        addToCart(item);
      })
      doc.appendChild(addToCartEl);
      document.querySelector(".main-section-products").appendChild(doc);
  })

  
}

getItems();