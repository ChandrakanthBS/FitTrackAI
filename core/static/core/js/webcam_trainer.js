// FitTrack AI - Advanced MediaPipe Biomechanical Pose Tracking & Multi-Exercise Form Coach
document.addEventListener('DOMContentLoaded', () => {
  const startWebcamBtn = document.getElementById('startWebcamTrainerBtn');
  const stopWebcamBtn = document.getElementById('stopWebcamTrainerBtn');
  const webcamModal = document.getElementById('webcamTrainerModal');
  const closeWebcamModal = document.getElementById('closeWebcamTrainerModal');
  
  const videoEl = document.getElementById('webcamVideo');
  const canvasEl = document.getElementById('webcamCanvas');
  const ctx = canvasEl ? canvasEl.getContext('2d') : null;

  const exerciseSelect = document.getElementById('aiTrainerExercise');
  const repCountEl = document.getElementById('aiRepCount');
  const accuracyEl = document.getElementById('aiAccuracyScore');
  const formFeedbackEl = document.getElementById('aiFormFeedback');
  const voiceToggleBtn = document.getElementById('aiVoiceToggle');
  const saveWorkoutBtn = document.getElementById('aiSaveWorkoutBtn');

  let cameraUtilsInstance = null;
  let poseInstance = null;
  let voiceEnabled = true;
  
  // Workout State
  let repCount = 0;
  let exerciseState = "UP"; // State machine for rep tracking
  let currentAccuracy = 100;
  let repAccuracies = []; // Array of scores per completed rep
  let smoothedLandmarks = null; // Exponential Moving Average smoothing
  let lastVoiceTime = 0;

  // Voice AI Coaching Speech Synthesis
  function speakRecommendation(text) {
    if (!voiceEnabled || !('speechSynthesis' in window)) return;
    
    const now = Date.now();
    if (now - lastVoiceTime < 3200) return; // Prevent rapid audio overlap
    lastVoiceTime = now;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  }

  // Toggle Voice AI Button
  if (voiceToggleBtn) {
    voiceToggleBtn.addEventListener('click', () => {
      voiceEnabled = !voiceEnabled;
      voiceToggleBtn.innerHTML = voiceEnabled 
        ? '<i class="fas fa-volume-high"></i> Voice AI: ON' 
        : '<i class="fas fa-volume-xmark"></i> Voice AI: OFF';
      voiceToggleBtn.classList.toggle('btn-primary', voiceEnabled);
      voiceToggleBtn.classList.toggle('btn-secondary', !voiceEnabled);
    });
  }

  // --- MATHEMATICAL & KINEMATIC HELPER FUNCTIONS ---

  // 1. Vector Angle Calculator (3 Points A, B, C -> Angle at vertex B in degrees)
  function calculateAngle(a, b, c) {
    if (!a || !b || !c) return 180;
    const radians = Math.atan2(c.y - b.y, c.x - b.x) - Math.atan2(a.y - b.y, a.x - b.x);
    let angle = Math.abs((radians * 180.0) / Math.PI);
    if (angle > 180.0) {
      angle = 360.0 - angle;
    }
    return angle;
  }

  // 2. Vertical Angle Calculator (Angle of line segment AB relative to vertical axis Y)
  function calculateVerticalAngle(a, b) {
    if (!a || !b) return 0;
    const dx = Math.abs(b.x - a.x);
    const dy = Math.abs(b.y - a.y);
    const radians = Math.atan2(dx, dy);
    return (radians * 180.0) / Math.PI;
  }

  // 3. Distance from Point P to Line Segment AB (Normalized spine alignment measurement)
  function calculatePointToLineDistance(p, a, b) {
    if (!p || !a || !b) return 0;
    const num = Math.abs((b.y - a.y) * p.x - (b.x - a.x) * p.y + b.x * a.y - b.y * a.x);
    const den = Math.sqrt(Math.pow(b.y - a.y, 2) + Math.pow(b.x - a.x, 2));
    return den === 0 ? 0 : num / den;
  }

  // 4. Euclidean Distance between two keypoints
  function calculateDistance(p1, p2) {
    if (!p1 || !p2) return 0;
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
  }

  // 5. Exponential Moving Average Landmark Smoother (Reduces MediaPipe Jitter)
  function smoothKeypoints(rawLandmarks, alpha = 0.35) {
    if (!smoothedLandmarks || smoothedLandmarks.length !== rawLandmarks.length) {
      smoothedLandmarks = rawLandmarks.map(p => ({ ...p }));
      return smoothedLandmarks;
    }
    for (let i = 0; i < rawLandmarks.length; i++) {
      smoothedLandmarks[i].x = (1 - alpha) * smoothedLandmarks[i].x + alpha * rawLandmarks[i].x;
      smoothedLandmarks[i].y = (1 - alpha) * smoothedLandmarks[i].y + alpha * rawLandmarks[i].y;
      smoothedLandmarks[i].z = (1 - alpha) * smoothedLandmarks[i].z + alpha * rawLandmarks[i].z;
    }
    return smoothedLandmarks;
  }

  // --- REAL-TIME ACCURACY DISPLAY UPDATE ---
  function updateAccuracyScoreUI(score) {
    currentAccuracy = Math.max(0, Math.min(100, Math.round(score)));
    if (!accuracyEl) return;
    
    // Overall display score (average of completed reps if available, or current rep)
    let displayScore = currentAccuracy;
    if (repAccuracies.length > 0) {
      const sum = repAccuracies.reduce((a, b) => a + b, 0);
      displayScore = Math.round(sum / repAccuracies.length);
    }
    
    accuracyEl.textContent = `${displayScore}%`;

    // Dynamic Color Styling
    if (displayScore >= 85) {
      accuracyEl.style.color = '#10B981'; // Emerald Green
    } else if (displayScore >= 70) {
      accuracyEl.style.color = '#F59E0B'; // Amber / Yellow
    } else {
      accuracyEl.style.color = '#E11D48'; // Rose Red
    }
  }


  // --- MAIN MEDIAPIPE FRAME PROCESSING FUNCTION ---
  function onResults(results) {
    if (!canvasEl || !ctx || !videoEl) return;

    const w = videoEl.videoWidth || 640;
    const h = videoEl.videoHeight || 480;

    if (canvasEl.width !== w || canvasEl.height !== h) {
      canvasEl.width = w;
      canvasEl.height = h;
    }

    ctx.save();
    ctx.clearRect(0, 0, w, h);

    // Mirror canvas horizontally to match mirrored video element
    ctx.translate(w, 0);
    ctx.scale(-1, 1);

    if (results.poseLandmarks && results.poseLandmarks.length > 0) {
      // Smooth keypoint coordinates for high accuracy tracking
      const landmarks = smoothKeypoints(results.poseLandmarks, 0.35);

      // Determine skeleton overlay color based on current accuracy score
      let skeletonColor = '#10B981'; // Green
      if (currentAccuracy < 70) {
        skeletonColor = '#E11D48'; // Red
      } else if (currentAccuracy < 85) {
        skeletonColor = '#F59E0B'; // Yellow
      }

      // Draw MediaPipe Pose Skeleton Connections
      if (window.drawConnectors && window.POSE_CONNECTIONS) {
        window.drawConnectors(ctx, landmarks, window.POSE_CONNECTIONS, {
          color: skeletonColor,
          lineWidth: 4
        });
      }
      if (window.drawLandmarks) {
        window.drawLandmarks(ctx, landmarks, {
          color: '#0284C7',
          fillColor: '#FFFFFF',
          lineWidth: 2,
          radius: 5
        });
      }

      // Key Landmark References
      const lShoulder = landmarks[11], rShoulder = landmarks[12];
      const lElbow = landmarks[13],    rElbow = landmarks[14];
      const lWrist = landmarks[15],    rWrist = landmarks[16];
      const lHip = landmarks[23],      rHip = landmarks[24];
      const lKnee = landmarks[25],     rKnee = landmarks[26];
      const lAnkle = landmarks[27],    rAnkle = landmarks[28];

      const selectedEx = exerciseSelect ? exerciseSelect.value : 'Squats';
      let frameAngleDisplay = 180;
      let frameAccuracy = 100;
      let feedbackText = "";
      let feedbackColor = 'var(--accent-emerald)';

      // -------------------------------------------------------------
      // EXERCISE 1: SQUATS (Depth, Torso Tilt, Knee Valgus)
      // -------------------------------------------------------------
      if (selectedEx === 'Squats') {
        const lKneeAngle = calculateAngle(lHip, lKnee, lAnkle);
        const rKneeAngle = calculateAngle(rHip, rKnee, rAnkle);
        const kneeAngle = (lKneeAngle + rKneeAngle) / 2;
        frameAngleDisplay = Math.round(kneeAngle);

        // Biomechanical Check 1: Torso Lean Angle (Shoulder to Hip vs Vertical)
        const midShoulder = { x: (lShoulder.x + rShoulder.x) / 2, y: (lShoulder.y + rShoulder.y) / 2 };
        const midHip = { x: (lHip.x + rHip.x) / 2, y: (lHip.y + rHip.y) / 2 };
        const torsoAngle = calculateVerticalAngle(midShoulder, midHip);

        // Biomechanical Check 2: Knee Valgus (Knee width vs Ankle width)
        const kneeDist = Math.abs(lKnee.x - rKnee.x);
        const ankleDist = Math.abs(lAnkle.x - rAnkle.x);
        const kneeValgusRatio = ankleDist > 0 ? kneeDist / ankleDist : 1.0;

        let penalties = 0;

        // Torso Penalty
        if (torsoAngle > 42) {
          penalties += 20;
          feedbackText = "Form Warning: Keep chest up! Avoid leaning torso too far forward.";
          feedbackColor = 'var(--accent-rose)';
        }

        // Knee Valgus Penalty
        if (kneeValgusRatio < 0.75) {
          penalties += 15;
          feedbackText = "Form Warning: Knees caving in! Push knees outward over your feet.";
          feedbackColor = 'var(--accent-amber)';
        }

        // State Machine & Rep Counting
        if (kneeAngle <= 105) { // Reached bottom of squat
          exerciseState = "DOWN";
          
          // Depth Check: 90 deg = 100% depth, >105 deg = depth penalty
          if (kneeAngle > 98) {
            penalties += 15;
            feedbackText = "Form Recommendation: Go lower! Lower hips to parallel for full rep.";
            feedbackColor = 'var(--accent-amber)';
          } else {
            feedbackText = "Excellent depth! Hold form and drive back up.";
            feedbackColor = 'var(--accent-emerald)';
          }
        } else if (kneeAngle > 155) { // Returned to top standing posture
          if (exerciseState === "DOWN") {
            repCount++;
            exerciseState = "UP";
            const finalRepScore = Math.max(50, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Great Squat! Rep ${repCount} completed (${finalRepScore}% accuracy).`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Rep ${repCount} complete! Perfect squat.`);
          }
        }

        frameAccuracy = 100 - penalties;
      }

      // -------------------------------------------------------------
      // EXERCISE 2: PUSHUPS (Chest Depth, Spine Alignment, Elbow Flare)
      // -------------------------------------------------------------
      else if (selectedEx === 'Pushups') {
        const lArmAngle = calculateAngle(lShoulder, lElbow, lWrist);
        const rArmAngle = calculateAngle(rShoulder, rElbow, rWrist);
        const armAngle = (lArmAngle + rArmAngle) / 2;
        frameAngleDisplay = Math.round(armAngle);

        // Biomechanical Check 1: Spine Alignment (Hip distance to Shoulder-Ankle line)
        const midShoulder = { x: (lShoulder.x + rShoulder.x) / 2, y: (lShoulder.y + rShoulder.y) / 2 };
        const midHip = { x: (lHip.x + rHip.x) / 2, y: (lHip.y + rHip.y) / 2 };
        const midAnkle = { x: (lAnkle.x + rAnkle.x) / 2, y: (lAnkle.y + rAnkle.y) / 2 };
        const spineDev = calculatePointToLineDistance(midHip, midShoulder, midAnkle);

        let penalties = 0;

        // Spine Sagging / Arching Penalty
        if (spineDev > 0.075) {
          penalties += 25;
          feedbackText = "Form Warning: Keep spine straight! Don't sag or arch hips.";
          feedbackColor = 'var(--accent-rose)';
        }

        // State Machine
        if (armAngle <= 95) { // Reached bottom chest drop
          exerciseState = "DOWN";
          
          if (armAngle > 88) {
            penalties += 10;
            feedbackText = "Go deeper! Lower chest closer to the ground.";
            feedbackColor = 'var(--accent-amber)';
          }
        } else if (armAngle > 155) { // Returned to top plank extension
          if (exerciseState === "DOWN") {
            repCount++;
            exerciseState = "UP";
            const finalRepScore = Math.max(50, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Pushup Rep ${repCount} completed! (${finalRepScore}% form score).`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Pushup rep ${repCount} complete!`);
          }
        }

        frameAccuracy = 100 - penalties;
      }

      // -------------------------------------------------------------
      // EXERCISE 3: BICEP CURLS (Elbow Isolation, Torso Sway, Full Extension)
      // -------------------------------------------------------------
      else if (selectedEx === 'Bicep Curls') {
        const lArmAngle = calculateAngle(lShoulder, lElbow, lWrist);
        const rArmAngle = calculateAngle(rShoulder, rElbow, rWrist);
        const armAngle = (lArmAngle + rArmAngle) / 2;
        frameAngleDisplay = Math.round(armAngle);

        // Biomechanical Check 1: Elbow Isolation (Elbow X displacement relative to Shoulder X)
        const elbowDrift = Math.abs(lElbow.x - lShoulder.x) + Math.abs(rElbow.x - rShoulder.x);

        // Biomechanical Check 2: Torso Sway Angle
        const midShoulder = { x: (lShoulder.x + rShoulder.x) / 2, y: (lShoulder.y + rShoulder.y) / 2 };
        const midHip = { x: (lHip.x + rHip.x) / 2, y: (lHip.y + rHip.y) / 2 };
        const torsoSway = calculateVerticalAngle(midShoulder, midHip);

        let penalties = 0;

        // Elbow Drift Penalty
        if (elbowDrift > 0.18) {
          penalties += 20;
          feedbackText = "Form Warning: Keep elbows pinned to your sides! Don't swing elbows forward.";
          feedbackColor = 'var(--accent-rose)';
        }

        // Torso Sway Penalty
        if (torsoSway > 20) {
          penalties += 20;
          feedbackText = "Form Warning: Avoid swinging upper body! Use arm power only.";
          feedbackColor = 'var(--accent-rose)';
        }

        // State Machine
        if (armAngle <= 60) { // Top of bicep squeeze
          exerciseState = "UP";
          feedbackText = "Good contraction at top! Lower down slowly under control.";
          feedbackColor = 'var(--accent-emerald)';
        } else if (armAngle > 140) { // Bottom full extension
          if (exerciseState === "UP") {
            repCount++;
            exerciseState = "DOWN";
            const finalRepScore = Math.max(50, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Bicep Curl Rep ${repCount} complete! (${finalRepScore}% accuracy).`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Rep ${repCount} complete! Solid bicep curl.`);
          }
        }

        frameAccuracy = 100 - penalties;
      }

      // -------------------------------------------------------------
      // EXERCISE 4: JUMPING JACKS (Overhead Arm Reach & Leg Spread Width)
      // -------------------------------------------------------------
      else if (selectedEx === 'Jumping Jacks') {
        const armsUp = lWrist.y < lShoulder.y && rWrist.y < rShoulder.y;
        const armsDown = lWrist.y > lHip.y && rWrist.y > rHip.y;

        const armAngle = (calculateAngle(lHip, lShoulder, lWrist) + calculateAngle(rHip, rShoulder, rWrist)) / 2;
        frameAngleDisplay = Math.round(armAngle);

        const legWidth = Math.abs(lAnkle.x - rAnkle.x);
        const shoulderWidth = Math.abs(lShoulder.x - rShoulder.x);
        const legSpreadRatio = shoulderWidth > 0 ? legWidth / shoulderWidth : 1.0;

        let penalties = 0;

        if (armsUp) {
          if (legSpreadRatio < 1.3) {
            penalties += 20;
            feedbackText = "Jump wider! Spread legs wider as arms reach overhead.";
            feedbackColor = 'var(--accent-amber)';
          }
          exerciseState = "OUT";
        } else if (armsDown) {
          if (exerciseState === "OUT") {
            repCount++;
            exerciseState = "IN";
            const finalRepScore = Math.max(60, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Jumping Jack Rep ${repCount} completed!`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Jack rep ${repCount}!`);
          }
        }

        frameAccuracy = 100 - penalties;
      }

      // -------------------------------------------------------------
      // EXERCISE 5: SHOULDER PRESS (Overhead Lockout & Elbow Drop Depth)
      // -------------------------------------------------------------
      else if (selectedEx === 'Shoulder Press') {
        const lArmAngle = calculateAngle(lShoulder, lElbow, lWrist);
        const rArmAngle = calculateAngle(rShoulder, rElbow, rWrist);
        const armAngle = (lArmAngle + rArmAngle) / 2;
        frameAngleDisplay = Math.round(armAngle);

        let penalties = 0;

        // Torso verticality check
        const midShoulder = { x: (lShoulder.x + rShoulder.x) / 2, y: (lShoulder.y + rShoulder.y) / 2 };
        const midHip = { x: (lHip.x + rHip.x) / 2, y: (lHip.y + rHip.y) / 2 };
        const torsoAngle = calculateVerticalAngle(midShoulder, midHip);

        if (torsoAngle > 18) {
          penalties += 20;
          feedbackText = "Form Warning: Keep core engaged! Avoid arching lower back.";
          feedbackColor = 'var(--accent-rose)';
        }

        if (armAngle > 155 && lWrist.y < lShoulder.y && rWrist.y < rShoulder.y) { // Full overhead press extension
          if (exerciseState === "DOWN") {
            repCount++;
            exerciseState = "UP";
            const finalRepScore = Math.max(50, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Shoulder Press Rep ${repCount} complete! (${finalRepScore}% accuracy).`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Shoulder press rep ${repCount} complete!`);
          }
        } else if (armAngle <= 95) { // Lowered down to shoulder level
          exerciseState = "DOWN";
        }

        frameAccuracy = 100 - penalties;
      }

      // -------------------------------------------------------------
      // EXERCISE 6: LUNGES (Front Knee Depth & Upright Torso)
      // -------------------------------------------------------------
      else if (selectedEx === 'Lunges') {
        const lKneeAngle = calculateAngle(lHip, lKnee, lAnkle);
        const rKneeAngle = calculateAngle(rHip, rKnee, rAnkle);
        // Identify active bending knee (smaller angle)
        const activeKneeAngle = Math.min(lKneeAngle, rKneeAngle);
        frameAngleDisplay = Math.round(activeKneeAngle);

        let penalties = 0;

        const midShoulder = { x: (lShoulder.x + rShoulder.x) / 2, y: (lShoulder.y + rShoulder.y) / 2 };
        const midHip = { x: (lHip.x + rHip.x) / 2, y: (lHip.y + rHip.y) / 2 };
        const torsoAngle = calculateVerticalAngle(midShoulder, midHip);

        if (torsoAngle > 22) {
          penalties += 20;
          feedbackText = "Form Warning: Keep upper body upright! Don't lean forward.";
          feedbackColor = 'var(--accent-rose)';
        }

        if (activeKneeAngle <= 100) {
          exerciseState = "DOWN";
          if (activeKneeAngle > 92) {
            penalties += 10;
            feedbackText = "Step deeper into your lunge for maximum leg activation.";
            feedbackColor = 'var(--accent-amber)';
          }
        } else if (activeKneeAngle > 150) {
          if (exerciseState === "DOWN") {
            repCount++;
            exerciseState = "UP";
            const finalRepScore = Math.max(50, 100 - penalties);
            repAccuracies.push(finalRepScore);
            if (repCountEl) repCountEl.textContent = repCount;

            feedbackText = `Lunge Rep ${repCount} completed! (${finalRepScore}% form score).`;
            feedbackColor = 'var(--accent-emerald)';
            speakRecommendation(`Lunge rep ${repCount} complete!`);
          }
        }

        frameAccuracy = 100 - penalties;
      }

      // Update Form Accuracy Score UI
      updateAccuracyScoreUI(frameAccuracy);

      // Render Feedback text to screen
      if (feedbackText && formFeedbackEl) {
        formFeedbackEl.textContent = feedbackText;
        formFeedbackEl.style.color = feedbackColor;
      }

      ctx.restore();

      // Render HUD Readout Banner on Canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
      ctx.fillRect(20, 20, 240, 64);
      ctx.strokeStyle = skeletonColor;
      ctx.lineWidth = 2;
      ctx.strokeRect(20, 20, 240, 64);

      ctx.fillStyle = '#10B981';
      ctx.font = 'bold 13px "JetBrains Mono", monospace';
      ctx.fillText(`EXERCISE: ${selectedEx.toUpperCase()}`, 32, 42);
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(`ANGLE: ${frameAngleDisplay}° | FORM: ${currentAccuracy}%`, 32, 64);
      return;

    } else {
      if (formFeedbackEl) {
        formFeedbackEl.textContent = "MediaPipe AI Searching for User... Position full body in camera frame.";
        formFeedbackEl.style.color = 'var(--accent-amber)';
      }
    }

    ctx.restore();
  }

  // --- INITIALIZE WEBCAM & MEDIAPIPE ENGINE ---
  async function startWebcam() {
    try {
      if (webcamModal) webcamModal.style.display = 'flex';
      
      repCount = 0;
      repAccuracies = [];
      exerciseState = "UP";
      smoothedLandmarks = null;
      if (repCountEl) repCountEl.textContent = '0';
      updateAccuracyScoreUI(100);

      if (!window.Pose) {
        alert('MediaPipe Pose AI module loading... Please try again in 3 seconds.');
        return;
      }

      poseInstance = new window.Pose({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
      });

      poseInstance.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      });

      poseInstance.onResults(onResults);

      if (window.Camera && videoEl) {
        cameraUtilsInstance = new window.Camera(videoEl, {
          onFrame: async () => {
            if (poseInstance && videoEl) {
              await poseInstance.send({ image: videoEl });
            }
          },
          width: 640,
          height: 480
        });

        await cameraUtilsInstance.start();
      } else {
        const userStream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoEl) {
          videoEl.srcObject = userStream;
          await videoEl.play();
        }
      }

      if (formFeedbackEl) {
        formFeedbackEl.textContent = 'MediaPipe AI Pose Engine Active. Video feed online! Begin exercising.';
        formFeedbackEl.style.color = 'var(--accent-emerald)';
      }

      speakRecommendation("MediaPipe AI Pose Engine active. High accuracy camera tracking initialized.");
    } catch (err) {
      console.error('MediaPipe Camera Error:', err);
      alert('Unable to access webcam. Please ensure camera permissions are allowed in browser settings.');
      if (webcamModal) webcamModal.style.display = 'none';
    }
  }

  // Stop Webcam Session
  function stopWebcam() {
    if (cameraUtilsInstance) {
      cameraUtilsInstance.stop();
      cameraUtilsInstance = null;
    }
    if (poseInstance) {
      poseInstance.close();
      poseInstance = null;
    }
    if (videoEl && videoEl.srcObject) {
      videoEl.srcObject.getTracks().forEach(track => track.stop());
      videoEl.srcObject = null;
    }
    if (webcamModal) webcamModal.style.display = 'none';
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
  }

  // Handle Exercise Selection Change
  if (exerciseSelect) {
    exerciseSelect.addEventListener('change', () => {
      repCount = 0;
      repAccuracies = [];
      exerciseState = "UP";
      if (repCountEl) repCountEl.textContent = '0';
      updateAccuracyScoreUI(100);
      speakRecommendation(`Switched tracking to ${exerciseSelect.value}. Rep count reset.`);
    });
  }

  // Save AI Session to Dashboard
  if (saveWorkoutBtn) {
    saveWorkoutBtn.addEventListener('click', async () => {
      if (repCount === 0) {
        alert("No repetitions completed yet! Perform some reps before saving.");
        return;
      }

      const exName = exerciseSelect ? exerciseSelect.value : 'Squats';
      const mins = Math.max(1, Math.round(repCount * 0.5));
      const cals = repCount * 6;

      // Calculate final average form accuracy
      let avgAccuracy = 100;
      if (repAccuracies.length > 0) {
        avgAccuracy = Math.round(repAccuracies.reduce((a, b) => a + b, 0) / repAccuracies.length);
      }

      const formData = new FormData();
      formData.append('submit_exercise', '1');
      formData.append('exercise_name', `AI Pose ${exName} (${avgAccuracy}% Form Accuracy)`);
      formData.append('category', 'HIIT');
      formData.append('duration_minutes', mins);
      formData.append('calories_burned', cals);
      formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]')?.value || '');

      try {
        await fetch('/dashboard/', { method: 'POST', body: formData });
        speakRecommendation(`Workout saved successfully! ${repCount} reps of ${exName} recorded at ${avgAccuracy} percent form accuracy.`);
        alert(`MediaPipe AI Workout Saved! ${repCount} reps of ${exName} (${avgAccuracy}% Form Accuracy) logged to your dashboard.`);
        stopWebcam();
        window.location.href = '/dashboard/';
      } catch (err) {
        alert(`Workout finished! ${repCount} reps logged.`);
        stopWebcam();
      }
    });
  }

  if (startWebcamBtn) startWebcamBtn.addEventListener('click', startWebcam);
  if (stopWebcamBtn) stopWebcamBtn.addEventListener('click', stopWebcam);
  if (closeWebcamModal) closeWebcamModal.addEventListener('click', stopWebcam);
});
