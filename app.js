// New Features
let powerUps = [];
let shieldActive = false;
let shieldDuration = 5000; // 5 seconds
let shieldTimer = 0;
let highScore = 0;

// Power-Up Image
const shieldImage = new Image();
shieldImage.src = "shield.png"; // Replace with your shield power-up image path

// Generate power-ups
function generatePowerUps() {
  if (Math.random() < 0.01) {
    let x = Math.random() * (canvas.width - 30);
    let y = -50;
    powerUps.push({ x, y, width: 30, height: 30, type: "shield" });
  }
}

// Move power-ups
function movePowerUps() {
  powerUps.forEach((powerUp, index) => {
    powerUp.y += 2;
    if (powerUp.y > canvas.height) {
      powerUps.splice(index, 1); // Remove off-screen power-ups
    }

    // Check collision with player car
    const playerRect = { x: playerCar.x, y: playerCar.y, width: playerCar.width, height: playerCar.height };
    const powerUpRect = { x: powerUp.x, y: powerUp.y, width: powerUp.width, height: powerUp.height };
    if (isCollision(playerRect, powerUpRect)) {
      if (powerUp.type === "shield") {
        shieldActive = true;
        shieldTimer = Date.now();
      }
      powerUps.splice(index, 1); // Remove collected power-up
    }
  });
}

// Draw power-ups
function drawPowerUps() {
  powerUps.forEach((powerUp) => {
    ctx.drawImage(shieldImage, powerUp.x, powerUp.y, powerUp.width, powerUp.height);
  });
}

// Update shield state
function updateShield() {
  if (shieldActive && Date.now() - shieldTimer > shieldDuration) {
    shieldActive = false;
  }

  if (shieldActive) {
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 3;
    ctx.strokeRect(playerCar.x - 5, playerCar.y - 5, playerCar.width + 10, playerCar.height + 10);
  }
}

// Update high score
function updateHighScore() {
  if (score > highScore) {
    highScore = score;
  }
  document.getElementById("highScore").textContent = `High Score: ${highScore}`;
}

// Add elements for score and high score in HTML
// <div id="highScore"></div>

// Update the game loop
function gameLoop() {
  if (isGameOver || isPaused) return;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawBackground();
  drawPlayerCar();
  drawEnemyCars();
  drawPowerUps();
  movePlayerCar();
  generateEnemyCars();
  moveEnemyCars();
  generatePowerUps();
  movePowerUps();
  detectCollisions();
  updateShield();
  updateHighScore();

  document.getElementById("score").textContent = `Score: ${score}`;
  document.getElementById("lives").textContent = `Lives: ${lives}`;

  gameInterval = requestAnimationFrame(gameLoop);
}

// Update collision logic to include shield
function detectCollisions() {
  const playerRect = { x: playerCar.x, y: playerCar.y, width: playerCar.width, height: playerCar.height };
  enemyCars.forEach((car, index) => {
    const enemyRect = { x: car.x, y: car.y, width: car.width, height: car.height };
    if (isCollision(playerRect, enemyRect)) {
      if (shieldActive) {
        enemyCars.splice(index, 1); // Shield protects the car
      } else {
        crashSound.play(); // Play collision sound
        lives--;
        enemyCars.splice(index, 1); // Remove collided car
        if (lives === 0) {
          gameOver();
        }
      }
    }
  });
}

// Initialize the high score display
document.getElementById("highScore").textContent = `High Score: ${highScore}`;
