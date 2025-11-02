import React, { useState } from 'react';
import CheckoutButton from './CheckoutButton';

const BotBuilder = () => {
  const [step, setStep] = useState(1);
  const [selectedTasks, setSelectedTasks] = useState([]);
  const [previewText, setPreviewText] = useState('Your bot preview will appear here...');
  const [tier, setTier] = useState('glacier');
  const [botName, setBotName] = useState('');
  const [tone, setTone] = useState('professional');

  const tasks = {
    basic: ['Email Management', 'Social Media Posting', 'Customer Support Chatbot', 'Calendar/Scheduling', 'Basic Data Entry'],
    intermediate: ['Lead Nurturing', 'Sales Automation', 'Marketing Campaigns', 'Inventory Management', 'Task Management'],
    advanced: ['OSINT Analysis', 'Network Scanning', 'Threat Detection', 'API Integrations', 'Advanced Data Analysis'],
    custom: ['Custom AI Workflow']
  };

  const handleTaskSelection = async (task) => {
    if (selectedTasks.includes(task)) return;
    setSelectedTasks([...selectedTasks, task]);
    try {
      const response = await fetch('https://api.droxai.com/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `Generate bot configuration for ${task}`, max_tokens: 500 })
      });
      const data = await response.json();
      setPreviewText(data.response || `Bot will handle: ${task}`);
    } catch (error) {
      setPreviewText(`Bot will handle: ${task}`);
    }
  };

  const handleNextStep = () => {
    if (step < 4) setStep(step + 1);
  };

  const handlePrevStep = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="bg-gray-100 text-gray-900 min-h-screen p-6">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="w-full md:w-1/2 p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Build Your Bot</h2>
          {step === 1 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Step 1: Select Tier</h3>
              <select
                className="w-full p-2 border rounded"
                value={tier}
                onChange={(e) => setTier(e.target.value)}
              >
                <option value="glacier">Glacier</option>
                <option value="hollow">Hollow</option>
                <option value="forge">Forge</option>
                <option value="brahma">Brahma</option>
              </select>
              <button
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                onClick={handleNextStep}
              >
                Next
              </button>
            </div>
          )}
          {step === 2 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Step 2: Name and Tone</h3>
              <input
                type="text"
                placeholder="Bot Name"
                className="w-full p-2 mb-4 border rounded"
                value={botName}
                onChange={(e) => setBotName(e.target.value)}
              />
              <select
                className="w-full p-2 border rounded"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
              >
                <option value="professional">Professional</option>
                <option value="friendly">Friendly</option>
                <option value="formal">Formal</option>
              </select>
              <div className="flex justify-between mt-4">
                <button
                  className="px-4 py-2 bg-gray-300 text-gray-900 rounded hover:bg-gray-400 transition"
                  onClick={handlePrevStep}
                >
                  Previous
                </button>
                <button
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                  onClick={handleNextStep}
                >
                  Next
                </button>
              </div>
            </div>
          )}
          {step === 3 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Step 3: Select Tasks</h3>
              {Object.entries(tasks).map(([category, taskList]) => (
                <div key={category}>
                  {task_limits[tier]["allowed_categories"].includes(category) && (
                    <>
                      <h4 className="text-md font-medium mt-2">{category.charAt(0).toUpperCase() + category.slice(1)}</h4>
                      {taskList.map((task) => (
                        <button
                          key={task}
                          className="block w-full text-left px-4 py-2 my-1 bg-blue-100 hover:bg-blue-200 rounded transition"
                          onClick={() => handleTaskSelection(task)}
                        >
                          {task}
                        </button>
                      ))}
                    </>
                  )}
                </div>
              ))}
              <div className="flex justify-between mt-4">
                <button
                  className="px-4 py-2 bg-gray-300 text-gray-900 rounded hover:bg-gray-400 transition"
                  onClick={handlePrevStep}
                >
                  Previous
                </button>
                <button
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
                  onClick={handleNextStep}
                >
                  Next
                </button>
              </div>
            </div>
          )}
          {step === 4 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Step 4: Review and Deploy</h3>
              <p><strong>Bot Name:</strong> {botName}</p>
              <p><strong>Tone:</strong> {tone.charAt(0).toUpperCase() + tone.slice(1)}</p>
              <p><strong>Tier:</strong> {tier.charAt(0).toUpperCase() + tier.slice(1)}</p>
              <p><strong>Selected Tasks:</strong> {selectedTasks.join(', ')}</p>
              <CheckoutButton tier={tier} />
              <button
                className="mt-4 px-4 py-2 bg-gray-300 text-gray-900 rounded hover:bg-gray-400 transition"
                onClick={handlePrevStep}
              >
                Previous
              </button>
            </div>
          )}
        </div>
        <div className="w-full md:w-1/2 p-6 bg-white rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Bot Preview</h3>
          <div className="border p-4 rounded-md h-64 overflow-y-auto">
            <p>{previewText}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const task_limits = {
  "glacier": {"max_tasks": Infinity, "allowed_categories": ["basic"]},
  "hollow": {"max_tasks": Infinity, "allowed_categories": ["basic", "intermediate"]},
  "forge": {"max_tasks": Infinity, "allowed_categories": ["basic", "intermediate", "advanced"]},
  "brahma": {"max_tasks": Infinity, "allowed_categories": ["basic", "intermediate", "advanced", "custom"]}
};

export default BotBuilder;
