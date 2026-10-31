import random
from flask import Flask, jsonify, render_template_string, request, session

app = Flask(__name__)
# A secret key is required for Flask sessions
app.secret_key = "hangman_super_secret_local_key"

# -------------------------------------------------------------
# Predefined list of 5 words (no external file or API needed)
# -------------------------------------------------------------
WORDS = ["python", "hangman", "computer", "developer", "keyboard"]
MAX_INCORRECT = 6


def get_game_state():
    """Initializes or retrieves the session game state."""
    if "word" not in session:
        reset_game()

    word = session["word"]
    guessed = session.get("guessed", [])
    incorrect = session.get("incorrect", 0)
    status = session.get("status", "playing")

    # Build masked display
    display = [letter if letter in guessed else "_" for letter in word]

    return {
        "display": display,
        "guessed": guessed,
        "incorrect": incorrect,
        "max_incorrect": MAX_INCORRECT,
        "remaining": MAX_INCORRECT - incorrect,
        "status": status,
        "word_length": len(word),
        "secret_word": word if status in ("won", "lost") else None,
    }


def reset_game():
    """Starts a new round with a random secret word."""
    session["word"] = random.choice(WORDS)
    session["guessed"] = []
    session["incorrect"] = 0
    session["status"] = "playing"


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(get_game_state())


@app.route("/api/guess", methods=["POST"])
def api_guess():
    data = request.get_json(force=True, silent=True) or {}
    letter = data.get("letter", "").strip().lower()

    if "word" not in session:
        reset_game()

    word = session["word"]
    guessed = session.setdefault("guessed", [])
    incorrect = session.get("incorrect", 0)
    status = session.get("status", "playing")

    if status != "playing":
        return jsonify({"success": False, "message": "Game is already over.", "state": get_game_state()})

    # Validation
    if len(letter) != 1 or not letter.isalpha():
        return jsonify({"success": False, "message": "Please enter a single alphabetical letter.", "state": get_game_state()})

    if letter in guessed:
        return jsonify({"success": False, "message": f"'{letter.upper()}' was already guessed.", "state": get_game_state()})

    # Record guess
    guessed.append(letter)
    session["guessed"] = guessed

    if letter in word:
        message = f"Nice! '{letter.upper()}' is in the word."
    else:
        incorrect += 1
        session["incorrect"] = incorrect
        message = f"Oops! '{letter.upper()}' is not in the word."

    # Check win
    if all(char in guessed for char in word):
        session["status"] = "won"
        message = f"Congratulations! You guessed the word '{word.upper()}'!"
    elif incorrect >= MAX_INCORRECT:
        session["status"] = "lost"
        message = f"Game Over! The word was '{word.upper()}'."

    session.modified = True
    return jsonify({
        "success": True,
        "message": message,
        "state": get_game_state()
    })


@app.route("/api/restart", methods=["POST"])
def api_restart():
    reset_game()
    return jsonify({"success": True, "message": "New game started!", "state": get_game_state()})


# -------------------------------------------------------------
# Clean, modern single-page HTML / CSS / JS UI
# -------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hangman Game | Localhost</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(30, 41, 59, 0.85);
            --card-border: rgba(255, 255, 255, 0.1);
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --accent-light: #818cf8;
            --success: #10b981;
            --danger: #ef4444;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 780px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
            padding: 32px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
        }

        header {
            text-align: center;
        }

        header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(to right, #a5b4fc, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        header p {
            color: var(--text-sub);
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .game-board {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-around;
            width: 100%;
            gap: 24px;
            flex-wrap: wrap;
        }

        /* SVG Hangman Graphic */
        .gallows-container {
            width: 200px;
            height: 220px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
        }

        svg {
            width: 180px;
            height: 200px;
            stroke: #cbd5e1;
            stroke-width: 4;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .scaffold {
            stroke: #64748b;
            stroke-width: 5;
        }

        .rope {
            stroke: #d97706;
            stroke-width: 3;
        }

        .body-part {
            stroke: #f43f5e;
            stroke-width: 4;
            transition: all 0.3s ease;
            opacity: 0;
        }

        .body-part.visible {
            opacity: 1;
        }

        /* Status and word display */
        .info-panel {
            flex: 1;
            min-width: 280px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }

        .stats-badge {
            display: flex;
            gap: 16px;
            width: 100%;
            justify-content: center;
        }

        .stat-item {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--card-border);
            padding: 8px 16px;
            border-radius: 12px;
            font-size: 0.85rem;
            color: var(--text-sub);
            text-align: center;
        }

        .stat-item strong {
            display: block;
            font-size: 1.1rem;
            color: var(--text-main);
        }

        .word-display {
            display: flex;
            gap: 12px;
            margin: 12px 0;
            flex-wrap: wrap;
            justify-content: center;
        }

        .letter-slot {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2rem;
            font-weight: 700;
            width: 44px;
            height: 54px;
            border-bottom: 4px solid var(--accent-light);
            background: rgba(15, 23, 42, 0.4);
            border-radius: 8px 8px 0 0;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            transition: all 0.2s;
        }

        .letter-slot.filled {
            color: #38bdf8;
            border-bottom-color: #38bdf8;
            animation: popIn 0.2s ease-out;
        }

        @keyframes popIn {
            0% { transform: scale(0.7); }
            100% { transform: scale(1); }
        }

        /* Message Banner */
        .message-box {
            min-height: 28px;
            font-size: 0.95rem;
            font-weight: 600;
            color: #e2e8f0;
            text-align: center;
            transition: all 0.2s;
        }

        .message-box.win {
            color: var(--success);
            font-size: 1.15rem;
        }

        .message-box.lose {
            color: var(--danger);
            font-size: 1.15rem;
        }

        /* Keyboard */
        .keyboard {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
            max-width: 620px;
        }

        .kb-row {
            display: flex;
            justify-content: center;
            gap: 6px;
        }

        .kb-key {
            background: #334155;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            font-size: 1rem;
            font-weight: 600;
            border-radius: 8px;
            width: 44px;
            height: 48px;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.15s ease;
            box-shadow: 0 3px 0 #1e293b;
        }

        .kb-key:hover:not(:disabled) {
            background: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 5px 0 #3730a3;
        }

        .kb-key:active:not(:disabled) {
            transform: translateY(2px);
            box-shadow: 0 1px 0 #3730a3;
        }

        .kb-key:disabled {
            cursor: not-allowed;
            opacity: 0.35;
            transform: none;
            box-shadow: none;
        }

        .kb-key.correct {
            background: #059669;
            opacity: 0.9;
        }

        .kb-key.wrong {
            background: #dc2626;
            opacity: 0.4;
        }

        /* Action Buttons */
        .actions {
            display: flex;
            gap: 16px;
            margin-top: 8px;
        }

        .btn-restart {
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
            transition: all 0.2s ease;
        }

        .btn-restart:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }

        .btn-restart:active {
            transform: translateY(1px);
        }

        footer {
            margin-top: 16px;
            color: #64748b;
            font-size: 0.8rem;
            text-align: center;
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <h1>Hangman Localhost</h1>
            <p>Guess the 5 predefined words one letter at a time (Max 6 misses)</p>
        </header>

        <div class="game-board">
            <!-- Hangman Vector Graphic with 6 body parts -->
            <div class="gallows-container">
                <svg viewBox="0 0 160 180">
                    <!-- Gallows structure -->
                    <line x1="20" y1="170" x2="140" y2="170" class="scaffold" />
                    <line x1="40" y1="170" x2="40" y2="20" class="scaffold" />
                    <line x1="40" y1="20" x2="110" y2="20" class="scaffold" />
                    <line x1="40" y1="50" x2="70" y2="20" class="scaffold" />
                    <line x1="110" y1="20" x2="110" y2="45" class="rope" />

                    <!-- Part 1: Head -->
                    <circle id="part-1" cx="110" cy="60" r="14" class="body-part" />
                    <!-- Part 2: Body / Torso -->
                    <line id="part-2" x1="110" y1="74" x2="110" y2="116" class="body-part" />
                    <!-- Part 3: Left Arm -->
                    <line id="part-3" x1="110" y1="86" x2="90" y2="104" class="body-part" />
                    <!-- Part 4: Right Arm -->
                    <line id="part-4" x1="110" y1="86" x2="130" y2="104" class="body-part" />
                    <!-- Part 5: Left Leg -->
                    <line id="part-5" x1="110" y1="116" x2="92" y2="148" class="body-part" />
                    <!-- Part 6: Right Leg -->
                    <line id="part-6" x1="110" y1="116" x2="128" y2="148" class="body-part" />
                </svg>
            </div>

            <!-- Stats & Word Slots -->
            <div class="info-panel">
                <div class="stats-badge">
                    <div class="stat-item">
                        <span>Attempts Left</span>
                        <strong id="stat-remaining">6 / 6</strong>
                    </div>
                    <div class="stat-item">
                        <span>Incorrect</span>
                        <strong id="stat-incorrect" style="color: #f43f5e;">0</strong>
                    </div>
                </div>

                <div class="word-display" id="word-display">
                    <!-- Letter blanks injected here -->
                </div>

                <div class="message-box" id="message-box">Pick a letter or use your keyboard!</div>
            </div>
        </div>

        <!-- Virtual Keyboard -->
        <div class="keyboard" id="keyboard">
            <!-- Generated dynamically in JS -->
        </div>

        <div class="actions">
            <button class="btn-restart" id="btn-restart">🔄 New Game</button>
        </div>
    </div>

    <footer>
        Running live on <strong>http://localhost:5000</strong> &bull; Python Flask Hangman
    </footer>

    <script>
        const KEYBOARD_ROWS = [
            ["q","w","e","r","t","y","u","i","o","p"],
            ["a","s","d","f","g","h","j","k","l"],
            ["z","x","c","v","b","n","m"]
        ];

        let gameState = null;

        function buildKeyboard() {
            const kb = document.getElementById("keyboard");
            kb.innerHTML = "";
            KEYBOARD_ROWS.forEach(row => {
                const rowDiv = document.createElement("div");
                rowDiv.className = "kb-row";
                row.forEach(letter => {
                    const btn = document.createElement("button");
                    btn.className = "kb-key";
                    btn.id = `key-${letter}`;
                    btn.textContent = letter;
                    btn.onclick = () => sendGuess(letter);
                    rowDiv.appendChild(btn);
                });
                kb.appendChild(rowDiv);
            });
        }

        function renderUI(state) {
            gameState = state;

            // 1. Render Hangman Body Parts (1 to 6)
            for (let i = 1; i <= 6; i++) {
                const part = document.getElementById(`part-${i}`);
                if (part) {
                    if (i <= state.incorrect) {
                        part.classList.add("visible");
                    } else {
                        part.classList.remove("visible");
                    }
                }
            }

            // 2. Render Stats
            document.getElementById("stat-remaining").textContent = `${state.remaining} / ${state.max_incorrect}`;
            document.getElementById("stat-incorrect").textContent = state.incorrect;

            // 3. Render Word Blanks
            const wordDisplay = document.getElementById("word-display");
            wordDisplay.innerHTML = "";
            state.display.forEach(char => {
                const slot = document.createElement("div");
                slot.className = `letter-slot ${char !== "_" ? "filled" : ""}`;
                slot.textContent = char !== "_" ? char : "";
                wordDisplay.appendChild(slot);
            });

            // 4. Update Keyboard Key States
            const guessedSet = new Set(state.guessed);
            document.querySelectorAll(".kb-key").forEach(btn => {
                const letter = btn.textContent.toLowerCase();
                if (guessedSet.has(letter) || state.status !== "playing") {
                    btn.disabled = true;
                    if (state.secret_word && state.secret_word.includes(letter)) {
                        btn.classList.add("correct");
                    } else if (guessedSet.has(letter)) {
                        btn.classList.add("wrong");
                    }
                } else {
                    btn.disabled = false;
                    btn.classList.remove("correct", "wrong");
                }
            });

            // 5. Status styling on messages
            const msgBox = document.getElementById("message-box");
            msgBox.className = "message-box";
            if (state.status === "won") {
                msgBox.classList.add("win");
                msgBox.innerHTML = `🎉 <strong>Victory!</strong> You guessed: <strong>${state.secret_word.toUpperCase()}</strong>`;
            } else if (state.status === "lost") {
                msgBox.classList.add("lose");
                msgBox.innerHTML = `💀 <strong>Game Over!</strong> The word was: <strong>${state.secret_word.toUpperCase()}</strong>`;
            }
        }

        async function fetchState() {
            try {
                const res = await fetch("/api/state");
                const state = await res.json();
                renderUI(state);
            } catch (err) {
                console.error("Failed to fetch state:", err);
            }
        }

        async function sendGuess(letter) {
            if (!gameState || gameState.status !== "playing") return;
            const msgBox = document.getElementById("message-box");
            try {
                const res = await fetch("/api/guess", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ letter })
                });
                const data = await res.json();
                if (data.state) {
                    renderUI(data.state);
                }
                if (data.message && data.state.status === "playing") {
                    msgBox.textContent = data.message;
                }
            } catch (err) {
                console.error("Error sending guess:", err);
            }
        }

        async function restartGame() {
            try {
                const res = await fetch("/api/restart", { method: "POST" });
                const data = await res.json();
                if (data.state) {
                    renderUI(data.state);
                    document.getElementById("message-box").textContent = "Fresh round! Pick a letter to start.";
                }
            } catch (err) {
                console.error("Error restarting:", err);
            }
        }

        // Physical Keyboard listener
        window.addEventListener("keydown", (e) => {
            const char = e.key.toLowerCase();
            if (/^[a-z]$/.test(char)) {
                sendGuess(char);
            }
        });

        document.getElementById("btn-restart").onclick = restartGame;

        buildKeyboard();
        fetchState();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    # Run the server on 0.0.0.0 so localhost is reachable
    app.run(host="127.0.0.1", port=5000, debug=False)
