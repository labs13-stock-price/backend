
exports.seed = function(knex, Promise) {
  
  return knex('basicUsers')
      .truncate()
      .then(function () {
          // Inserts seed entries
          return knex('basicUsers').insert([
            {firstName:"Lajawanti",lastName:"Dhake",userName:"lajawanti",email:"abc@gmail.com",password:"test"},
            {firstName:"Zach",lastName:"Angell",userName:"zach",email:"def@gmail.com",password:"test"},
            {firstName:"Dmitriy",lastName:"Kavyazin",userName:"dmitriy",email:"ghi@gmail.com",password:"test"},
            {firstName:"Jason",lastName:"Pham",userName:"jason",email:"jkl@gmail.com",password:"test"}, 
            {firstName:"Derek",lastName:"Shing",userName:"derek",email:"mno@gmail.com",password:"test"},            
            {firstName:"Alex",lastName:"Crown",userName:"alex",email:"pqr@gmail.com",password:"test"},            
            {firstName:"Kris",lastName:"Roebuck",userName:"kris",email:"stu@gmail.com",password:"test"},            
            {firstName:"Tina",lastName:"Chauhan",userName:"tina",email:"wx@gmail.com",password:"test"},            
            {firstName:"Nydia",lastName:"Pharo",userName:"nydia",email:"yz@gmail.com",password:"test"},  
            {firstName:"Lucie",lastName:"Blackstone",userName:"Lucie",email:"abc_xyz@gmail.com",password:"test"},            
            {firstName:"Jina",lastName:"Bendig",userName:"jina",email:"ln_o@gmail.com",password:"test"},            
            {firstName:"Abhay",lastName:"Dev",userName:"abhay",email:"ab_jo@gmail.com",password:"test"},                      
      ]);
    });
};
