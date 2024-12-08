// Game setup
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Game variables
let playerCar = { x: 175, y: 500, width: 50, height: 80, speed: 5 };
let enemyCars = [];
let score = 0;
let lives = 3;
let gameInterval;
let isGameOver = false;

// Load assets
const playerCarImage = new Image();
playerCarImage.src = "player_car.png"; // Replace with your car image path

const enemyCarImage = new Image();
enemyCarImage.src = "enemy_car.png"; // Replace with your enemy car image path

// Draw player car
function drawPlayerCar() {
  ctx.drawImage(playerCarImage, playerCar.x, playerCar.y, playerCar.width, playerCar.height);
}

// Draw enemy cars
function drawEnemyCars() {
  enemyCars.forEach(car => {
    ctx.drawImage(enemyCarImage, car.x, car.y, car.width, car.height);
  });
}

// Move the player car
function movePlayerCar() {
  const keys = Object.keys(keysDown);
  if (keys.includes("ArrowLeft") && playerCar.x > 50) {
    playerCar.x -= playerCar.speed;
  }
  if (keys.includes("ArrowRight") && playerCar.x < canvas.width - playerCar.width - 50) {
    playerCar.x += playerCar.speed;
  }
}

// Generate new enemy cars
function generateEnemyCars() {
  if (Math.random() < 0.02) {
    let x = Math.floor(Math.random() * (canvas.width - 50)) + 50;
    let y = -100;
    enemyCars.push({ x, y, width: 50, height: 80, speed: 3 + score / 10 });
  }
}

// Move enemy cars
function moveEnemyCars() {
  for (let i = 0; i < enemyCars.length; i++) {
    enemyCars[i].y += enemyCars[i].speed;

    if (enemyCars[i].y > canvas.height) {
      enemyCars.splice(i, 1);
      score++;
      if (score % 5 === 0) {
        enemyCars.forEach(car => car.speed += 0.5); // Increase speed of all enemies every 5 points
      }
    }
  }
}

// Detect collisions
function detectCollisions() {
  const playerRect = { x: playerCar.x, y: playerCar.y, width: playerCar.width, height: playerCar.height };
  enemyCars.forEach(car => {
    const enemyRect = { x: car.x, y: car.y, width: car.width, height: car.height };
    if (isCollision(playerRect, enemyRect)) {
      lives--;
      enemyCars.splice(enemyCars.indexOf(car), 1); // Remove the collided enemy car
      if (lives === 0) {
        gameOver();
      }
    }
  });
}

// Check for collision between two rectangles
function isCollision(rect1, rect2) {
  return rect1.x < rect2.x + rect2.width &&
    rect1.x + rect1.width > rect2.x &&
    rect1.y < rect2.y + rect2.height &&
    rect1.y + rect1.height > rect2.y;
}

// Game over logic
function gameOver() {
  isGameOver = true;
  document.getElementById("gameOver").style.display = "block";
  document.getElementById("gameOver").querySelector("div").innerHTML = `Game Over! <br> Score: ${score}`;
}

// Restart the game
function restartGame() {
  score = 0;
  lives = 3;
  enemyCars = [];
  isGameOver = false;
  document.getElementById("gameOver").style.display = "none";
  gameLoop();
}

// Game loop
function gameLoop() {
  if (isGameOver) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  drawPlayerCar();
  drawEnemyCars();
  movePlayerCar();
  generateEnemyCars();
  moveEnemyCars();
  detectCollisions();

  document.getElementById("score").textContent = `Score: ${score}`;
  document.getElementById("lives").textContent = `Lives: ${lives}`;
  
  requestAnimationFrame(gameLoop);
}

// Set up key listener for player car movement
let keysDown = {};
window.addEventListener("keydown", (e) => {
  keysDown[e.key] = true;
});
window.addEventListener("keyup", (e) => {
  delete keysDown[e.key];
});

// Initialize game and start loop
document.getElementById("restartBtn").addEventListener("click", restartGame);
gameLoop();
