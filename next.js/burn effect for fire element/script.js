const canvas = document.getElementById("burnCanvas");
const ctx = canvas.getContext("2d");

// =========================
// CANVAS SETUP
// =========================
function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  // paint the dark cover ONLY ONCE
  ctx.globalCompositeOperation = "source-over";
  ctx.fillStyle = "#111";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

resize();
window.addEventListener("resize", resize);


// =========================
// PARTICLES
// =========================
let particles = [];

class Particle {
  constructor(x, y) {
    this.x = x;
    this.y = y;

    this.radius = Math.random() * 80 + 40; // bigger holes
    this.life = 1;
    this.decay = Math.random() * 0.02 + 0.01;

    this.vy = -2 - Math.random() * 2; // move upward
  }

  update() {
    this.life -= this.decay;
    this.y += this.vy;
  }

  draw() {
    // ERASE mode
    ctx.globalCompositeOperation = "destination-out";

    const g = ctx.createRadialGradient(
      this.x, this.y, 0,
      this.x, this.y, this.radius
    );

    g.addColorStop(0, "rgba(0,0,0,1)");
    g.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = g;

    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
  }
}


// =========================
// SPAWN FIRE FROM BOTTOM
// =========================
function spawn() {
  for (let i = 0; i < 10; i++) {
    particles.push(
      new Particle(
        Math.random() * canvas.width,
        canvas.height - 10
      )
    );
  }
}


// =========================
// ANIMATION LOOP
// =========================
function animate() {
  spawn();

  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];

    p.update();
    p.draw();

    if (p.life <= 0) particles.splice(i, 1);
  }

  requestAnimationFrame(animate);
}

animate();
