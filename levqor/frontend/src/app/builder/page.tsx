'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface Template {
  id: string
  name: string
  description: string
  category: string
  estimated_credits: number
}

interface WorkflowStep {
  id: string
  type: string
  connector: string
  params: Record<string, any>
}

export default function WorkflowBuilderPage() {
  const router = useRouter()
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null)
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    try {
      const backendBase = process.env.NEXT_PUBLIC_BACKEND_BASE || 'http://localhost:5000'
      const response = await fetch(`${backendBase}/api/v1/templates`)
      const data = await response.json()
      setTemplates(data.templates || [])
    } catch (error) {
      console.error('Failed to fetch templates:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadTemplate = (templateId: string) => {
    setSelectedTemplate(templateId)
    const template = templates.find(t => t.id === templateId)
    if (template) {
      setWorkflowSteps([{
        id: '1',
        type: 'action',
        connector: 'slack',
        params: {}
      }])
    }
  }

  const addStep = () => {
    const newStep: WorkflowStep = {
      id: String(workflowSteps.length + 1),
      type: 'action',
      connector: 'slack',
      params: {}
    }
    setWorkflowSteps([...workflowSteps, newStep])
  }

  const removeStep = (stepId: string) => {
    setWorkflowSteps(workflowSteps.filter(s => s.id !== stepId))
  }

  const updateStep = (stepId: string, field: string, value: any) => {
    setWorkflowSteps(workflowSteps.map(step => 
      step.id === stepId ? { ...step, [field]: value } : step
    ))
  }

  const saveWorkflow = async () => {
    setSaving(true)
    try {
      alert('Workflow saved! (Backend integration pending)')
      router.push('/dashboard')
    } catch (error) {
      console.error('Failed to save workflow:', error)
      alert('Failed to save workflow')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>Loading templates...</div>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Workflow Builder</h1>
        <p style={styles.subtitle}>Create automated workflows visually</p>
      </div>

      <div style={styles.content}>
        <div style={styles.sidebar}>
          <h3 style={styles.sidebarTitle}>Templates</h3>
          <div style={styles.templateList}>
            {templates.map(template => (
              <div
                key={template.id}
                style={{
                  ...styles.templateCard,
                  ...(selectedTemplate === template.id ? styles.templateCardActive : {})
                }}
                onClick={() => loadTemplate(template.id)}
              >
                <div style={styles.templateName}>{template.name}</div>
                <div style={styles.templateDesc}>{template.description}</div>
                <div style={styles.templateMeta}>
                  <span style={styles.badge}>{template.category}</span>
                  <span style={styles.credits}>{template.estimated_credits} credits</span>
                </div>
              </div>
            ))}
          </div>
          
          <div style={styles.sectionDivider}></div>
          
          <h3 style={styles.sidebarTitle}>Available Actions</h3>
          <div style={styles.actionList}>
            <div style={styles.actionItem}>📨 Send Slack Message</div>
            <div style={styles.actionItem}>📝 Create Notion Page</div>
            <div style={styles.actionItem}>✉️ Send Email</div>
            <div style={styles.actionItem}>🤖 AI Summarize</div>
            <div style={styles.actionItem}>🔁 Filter/Transform</div>
          </div>
        </div>

        <div style={styles.canvas}>
          <div style={styles.canvasHeader}>
            <h2 style={styles.canvasTitle}>Workflow Steps</h2>
            <button style={styles.addButton} onClick={addStep}>
              + Add Step
            </button>
          </div>

          {workflowSteps.length === 0 ? (
            <div style={styles.emptyState}>
              <p>No steps yet. Select a template or add a step to get started.</p>
            </div>
          ) : (
            <div style={styles.stepsList}>
              {workflowSteps.map((step, index) => (
                <div key={step.id} style={styles.stepCard}>
                  <div style={styles.stepHeader}>
                    <span style={styles.stepNumber}>Step {index + 1}</span>
                    <button 
                      style={styles.removeButton}
                      onClick={() => removeStep(step.id)}
                    >
                      ✕
                    </button>
                  </div>
                  
                  <div style={styles.stepForm}>
                    <div style={styles.formGroup}>
                      <label style={styles.label}>Action Type</label>
                      <select 
                        style={styles.select}
                        value={step.type}
                        onChange={(e) => updateStep(step.id, 'type', e.target.value)}
                      >
                        <option value="action">Action</option>
                        <option value="filter">Filter</option>
                        <option value="transform">Transform</option>
                      </select>
                    </div>

                    <div style={styles.formGroup}>
                      <label style={styles.label}>Connector</label>
                      <select 
                        style={styles.select}
                        value={step.connector}
                        onChange={(e) => updateStep(step.id, 'connector', e.target.value)}
                      >
                        <option value="slack">Slack</option>
                        <option value="notion">Notion</option>
                        <option value="gmail">Gmail</option>
                        <option value="ai">AI</option>
                      </select>
                    </div>

                    <div style={styles.formGroup}>
                      <label style={styles.label}>Configuration</label>
                      <textarea 
                        style={styles.textarea}
                        placeholder='{"channel": "#general", "message": "Hello"}'
                        defaultValue={JSON.stringify(step.params, null, 2)}
                        onChange={(e) => {
                          try {
                            const params = JSON.parse(e.target.value)
                            updateStep(step.id, 'params', params)
                          } catch (err) {
                            // Invalid JSON, ignore
                          }
                        }}
                      />
                    </div>
                  </div>

                  {index < workflowSteps.length - 1 && (
                    <div style={styles.arrow}>↓</div>
                  )}
                </div>
              ))}
            </div>
          )}

          {workflowSteps.length > 0 && (
            <div style={styles.actions}>
              <button 
                style={styles.saveButton}
                onClick={saveWorkflow}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Workflow'}
              </button>
              <button 
                style={styles.cancelButton}
                onClick={() => router.push('/dashboard')}
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f9fafb',
  },
  header: {
    backgroundColor: 'white',
    borderBottom: '1px solid #e5e7eb',
    padding: '1.5rem 2rem',
  },
  title: {
    fontSize: '1.875rem',
    fontWeight: 'bold',
    color: '#111827',
    margin: 0,
  },
  subtitle: {
    color: '#6b7280',
    marginTop: '0.5rem',
  },
  content: {
    display: 'flex',
    gap: '1.5rem',
    padding: '1.5rem',
    maxWidth: '1400px',
    margin: '0 auto',
  },
  sidebar: {
    width: '300px',
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '1.5rem',
    height: 'fit-content',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  sidebarTitle: {
    fontSize: '1.125rem',
    fontWeight: '600',
    marginBottom: '1rem',
    color: '#374151',
  },
  templateList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem',
  },
  templateCard: {
    padding: '0.75rem',
    border: '1px solid #e5e7eb',
    borderRadius: '6px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  templateCardActive: {
    borderColor: '#3b82f6',
    backgroundColor: '#eff6ff',
  },
  templateName: {
    fontWeight: '600',
    fontSize: '0.875rem',
    marginBottom: '0.25rem',
  },
  templateDesc: {
    fontSize: '0.75rem',
    color: '#6b7280',
    marginBottom: '0.5rem',
  },
  templateMeta: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  badge: {
    fontSize: '0.75rem',
    padding: '0.125rem 0.5rem',
    backgroundColor: '#dbeafe',
    color: '#1e40af',
    borderRadius: '9999px',
  },
  credits: {
    fontSize: '0.75rem',
    color: '#059669',
    fontWeight: '600',
  },
  sectionDivider: {
    height: '1px',
    backgroundColor: '#e5e7eb',
    margin: '1.5rem 0',
  },
  actionList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  actionItem: {
    padding: '0.5rem 0.75rem',
    fontSize: '0.875rem',
    backgroundColor: '#f9fafb',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  canvas: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '1.5rem',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  canvasHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  canvasTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#111827',
  },
  addButton: {
    padding: '0.5rem 1rem',
    backgroundColor: '#3b82f6',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.875rem',
    fontWeight: '500',
  },
  emptyState: {
    textAlign: 'center' as const,
    padding: '3rem',
    color: '#9ca3af',
  },
  stepsList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  stepCard: {
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    padding: '1rem',
    backgroundColor: '#fafafa',
  },
  stepHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  stepNumber: {
    fontWeight: '600',
    color: '#374151',
  },
  removeButton: {
    background: 'none',
    border: 'none',
    color: '#ef4444',
    cursor: 'pointer',
    fontSize: '1.25rem',
  },
  stepForm: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1rem',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: '500',
    color: '#374151',
  },
  select: {
    padding: '0.5rem',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '0.875rem',
    backgroundColor: 'white',
  },
  textarea: {
    padding: '0.5rem',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '0.75rem',
    fontFamily: 'monospace',
    minHeight: '100px',
    resize: 'vertical' as const,
  },
  arrow: {
    textAlign: 'center' as const,
    fontSize: '1.5rem',
    color: '#9ca3af',
    marginTop: '0.5rem',
  },
  actions: {
    display: 'flex',
    gap: '0.75rem',
    marginTop: '1.5rem',
    paddingTop: '1.5rem',
    borderTop: '1px solid #e5e7eb',
  },
  saveButton: {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#059669',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.875rem',
    fontWeight: '600',
  },
  cancelButton: {
    padding: '0.75rem 1.5rem',
    backgroundColor: 'white',
    color: '#6b7280',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.875rem',
  },
  loading: {
    textAlign: 'center' as const,
    padding: '3rem',
    color: '#6b7280',
  },
}
