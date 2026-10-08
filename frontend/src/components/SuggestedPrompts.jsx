import { SUGGESTED_PROMPTS } from '../data/suggestedPrompts'

export default function SuggestedPrompts({ onSelect, disabled }) {
  return (
    <div className="prompts" role="group" aria-label="Suggested prompts">
      {SUGGESTED_PROMPTS.map((prompt) => (
        <button
          type="button"
          key={prompt.id}
          className="prompt-chip"
          disabled={disabled}
          onClick={() => onSelect(prompt.message)}
        >
          <span className="prompt-icon" aria-hidden="true">{prompt.icon}</span>
          {prompt.label}
        </button>
      ))}
    </div>
  )
}
