(() => {
  const scenarios = [
    {
      name: 'After mistakes', context: 'A turnover follows the athlete into the next possession.',
      steps: [
        ['What happened, and what are you carrying into this next rep?', 'Name the mistake and the reaction in one sentence. Separate the last play from the next assignment.'],
        ['One easy breath. Release your shoulders. This possession starts here.', 'Practice a brief reset at the sideline, then repeat it after a simulated mistake.'],
        ['What is the one thing your coach needs from you next?', 'Choose one controllable cue, such as “find my assignment.” Keep the cue aligned with the head coach’s instruction.'],
        ['Eyes up. Find your spot. Talk to your teammate.', 'Rejoin the drill and rehearse the first physical action that returns attention to the team.'],
        ['Commit to this play. We will review the response after the rep.', 'Run several repetitions with a mistake built in. Debrief the response with the athlete and coach, and choose one cue to reuse.']
      ]
    },
    {
      name: 'Pressure moments', context: 'A late-game situation makes a familiar task feel bigger.',
      steps: [
        ['What feels different right now: the task, or what the result might mean?', 'Identify the pressure trigger in a coach-selected game situation.'],
        ['Easy breath. Feel your feet. Let the next action be simple.', 'Rehearse a short reset before repeating the pressure situation.'],
        ['What part of this play can you control?', 'Select one task cue from the coach’s instruction rather than a score or outcome target.'],
        ['Get set. Call your assignment. Start your routine.', 'Return to the drill with the same preparation routine used in ordinary repetitions.'],
        ['Trust the cue and finish the action.', 'Repeat with a clock or score condition. Debrief whether the athlete followed the cue, then agree on its next use.']
      ]
    },
    {
      name: 'Focus & composure', context: 'A disputed call pulls attention away from the next assignment.',
      steps: [
        ['Where is your attention right now?', 'Identify what took attention away and ask the athlete what they noticed.'],
        ['Pause. Easy breath. Bring your eyes back here.', 'Practice interrupting the reaction during an appropriate break.'],
        ['What is your next assignment?', 'Have the athlete repeat one clear instruction from the coach.'],
        ['Turn toward the play. Find your teammate. Communicate.', 'Rehearse a visible return to the task without arguing about the previous call.'],
        ['Follow through on that assignment for this rep.', 'Add a realistic distraction to the drill. Debrief attention, communication, and follow-through with the coach.']
      ]
    },
    {
      name: 'Role adjustment', context: 'An athlete’s playing time or assignment has changed.',
      steps: [
        ['What feels hardest about your role today?', 'Let the athlete name the challenge without guessing what their body language means.'],
        ['Take a breath. We can acknowledge that and still prepare.', 'Practice a reset before a substitution or a new drill assignment.'],
        ['What does your coach need from this role right now?', 'Use a responsibility confirmed by the head coach. Do not promise playing time.'],
        ['Show me the first action that helps the team in this role.', 'Rehearse entering the drill, communicating, or preparing on the sideline as appropriate.'],
        ['Do that job fully for this next rep.', 'Repeat the assigned role and debrief one useful contribution. Agree with the coach on the cue to reinforce.']
      ]
    },
    {
      name: 'Back from injury / slump', context: 'An athlete hesitates during an approved practice task after time away or a difficult stretch.',
      steps: [
        ['What are you noticing before this rep?', 'Ask about hesitation without assuming its cause. After injury, use only activities cleared by the medical team; pain or new symptoms go back to that team.'],
        ['Easy breath. We only need this approved step right now.', 'Rehearse a reset within the existing return-to-play plan or coach-selected drill.'],
        ['Which cue helps you carry out this task?', 'Choose one process cue. Avoid promises about recovery, results, or confidence.'],
        ['Take your position and begin the agreed movement.', 'Rejoin only the assigned, approved activity. The coach and medical team retain their roles.'],
        ['Finish the task, then tell us what you noticed.', 'Repeat within the agreed limits, debrief the response, and choose the next cue with the coach. This is not rehabilitation or medical clearance.']
      ]
    },
    {
      name: 'Performance anxiety', context: 'Pre-play nerves make it difficult to commit to a familiar action.',
      steps: [
        ['What are you noticing, and what is your attention stuck on?', 'Let the athlete describe ordinary performance nerves in their own words. This walkthrough is performance coaching, not diagnosis or therapy.'],
        ['Take an easy breath and feel your feet on the floor.', 'Rehearse a comfortable, brief reset without requiring the nerves to disappear.'],
        ['What is one useful action you can choose right now?', 'Pick a manageable task cue that supports the head coach’s instruction.'],
        ['Find your starting position. Connect with your teammate.', 'Return to a manageable practice repetition with the athlete’s input.'],
        ['Commit to the cue for this rep. Then we will check in.', 'Debrief the chosen action rather than demanding calm. Persistent or overwhelming distress belongs with a qualified mental-health professional.']
      ]
    }
  ];
  const names = ['Find It', 'Reset', 'Anchor', 'Move', 'Execute'];
  const times = ['0–5', '5–10', '10–15', '15–20', '20–30'];
  let scenario = 0, step = 0;
  const choices = [...document.querySelectorAll('[data-scenario]')];
  const previous = document.getElementById('session-previous');
  const next = document.getElementById('session-next');
  if (!previous || !next) return;
  function render() {
    const selected = scenarios[scenario];
    document.getElementById('session-scenario').textContent = selected.name.toUpperCase();
    document.getElementById('session-context').textContent = selected.context;
    document.getElementById('session-clock').textContent = `SESSION CLOCK · ${times[step]} MINUTES · STEP ${step + 1} OF 5`;
    document.getElementById('session-step').textContent = names[step];
    document.getElementById('session-script').textContent = `“${selected.steps[step][0]}”`;
    document.getElementById('session-action').textContent = selected.steps[step][1];
    previous.disabled = step === 0;
    next.textContent = step === 4 ? 'Restart scenario ↺' : `Next: ${names[step + 1]} →`;
    choices.forEach((button, index) => button.setAttribute('aria-pressed', String(index === scenario)));
  }
  choices.forEach((button, index) => button.addEventListener('click', () => { scenario = index; step = 0; render(); }));
  previous.addEventListener('click', () => { step = Math.max(0, step - 1); render(); });
  next.addEventListener('click', () => { step = (step + 1) % names.length; render(); });
  render();
})();
