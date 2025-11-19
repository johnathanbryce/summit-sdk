import { useState, useEffect, useRef } from 'react'
import {
  Container,
  Title,
  Text,
  Paper,
  Stack,
  Group,
  TextInput,
  Button,
  Box,
  SegmentedControl,
} from '@mantine/core'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
interface Message {
  role: 'user' | 'assistant'
  content: string
}

type InputType = 'summary' | 'chat'

const App = () => {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [inputType, setInputType] = useState<InputType>('summary')
  const [chatTokens, setChatTokens] = useState({ input: 0, output: 0, total: 0 })
  const [summaryTokens, setSummaryTokens] = useState({ input: 0, output: 0, total: 0 })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
    }
    setMessages((prev) => [...prev, userMessage])

    try {
      setIsLoading(true)
      const endpoint = inputType === 'chat' ? '/chat' : '/summarize'

      const conversationHistory = [...messages, userMessage].map((msg) => ({
        role: msg.role,
        content: msg.content,
      }))

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: conversationHistory,
          respondInLanguage: null,
        }),
      })

      const data = await response.json()

      if (data.response) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { role: data.role, content: data.response },
        ])
        setInput('')

        // update token tracking
        if (data.usage) {
          const updateFunc = inputType === 'chat' ? setChatTokens : setSummaryTokens
          updateFunc((prev) => ({
            input: prev.input + data.usage.input_tokens,
            output: prev.output + data.usage.output_tokens,
            total: prev.total + data.usage.total_tokens,
          }))
        }
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Container size="lg" py="xl">
      <Stack gap="lg" mb="xl" ta="center">
        <Title order={1}>Summit SDK Demo</Title>
        <Text c="dimmed">AI-powered content querying</Text>

        <Group justify="center" gap="xl">
          <Box>
            <Text size="xs" c="dimmed" ta="center">
              Chat Tokens
            </Text>
            <Text size="sm" fw={500} ta="center">
              {chatTokens.total.toLocaleString()}
            </Text>
          </Box>
          <Box>
            <Text size="xs" c="dimmed" ta="center">
              Summary Tokens
            </Text>
            <Text size="sm" fw={500} ta="center">
              {summaryTokens.total.toLocaleString()}
            </Text>
          </Box>
        </Group>
      </Stack>

      <Paper shadow="sm" radius="md" withBorder>
        <Box
          h={600}
          p="md"
          style={{ overflowY: 'auto', backgroundColor: 'var(--mantine-color-gray-0)' }}
        >
          {messages.length === 0 ? (
            <Text c="dimmed" ta="center" py="xl">
              No messages yet. Start a conversation below.
            </Text>
          ) : (
            <Stack gap="sm">
              {messages.map((message, index) => (
                <Box
                  key={index}
                  p="sm"
                  style={{
                    maxWidth: '80%',
                    marginLeft: message.role === 'user' ? 'auto' : 0,
                    marginRight: message.role === 'user' ? 0 : 'auto',
                    backgroundColor:
                      message.role === 'user'
                        ? 'var(--mantine-color-blue-6)'
                        : 'var(--mantine-color-white)',
                    color: message.role === 'user' ? 'white' : 'inherit',
                    borderRadius: 'var(--mantine-radius-md)',
                    border:
                      message.role === 'assistant'
                        ? '1px solid var(--mantine-color-gray-3)'
                        : 'none',
                  }}
                >
                  <Group justify="space-between" mb={4}>
                    <Text size="xs" fw={600} opacity={0.8}>
                      {message.role === 'user' ? 'You' : 'Assistant'}
                    </Text>
                  </Group>
                  <Text size="sm">{message.content}</Text>
                </Box>
              ))}
              {isLoading && (
                <Box
                  p="sm"
                  style={{
                    maxWidth: '80%',
                    backgroundColor: 'var(--mantine-color-white)',
                    borderRadius: 'var(--mantine-radius-md)',
                    border: '1px solid var(--mantine-color-gray-3)',
                  }}
                >
                  <Text size="sm">●●●</Text>
                </Box>
              )}
              <div ref={messagesEndRef} />
            </Stack>
          )}
        </Box>

        <Box p="md" style={{ borderTop: '1px solid var(--mantine-color-gray-3)' }}>
          <Stack gap="md">
            <Group justify="center">
              <SegmentedControl
                value={inputType}
                onChange={(value) => setInputType(value as InputType)}
                data={[
                  { label: 'Summarize', value: 'summary' },
                  { label: 'Chat', value: 'chat' },
                ]}
              />
            </Group>

            <form onSubmit={handleSubmit}>
              <Group gap="xs">
                <TextInput
                  flex={1}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder={
                    inputType === 'chat'
                      ? 'Ask a question...'
                      : 'Input text or a URL for a summary...'
                  }
                  disabled={isLoading}
                />
                <Button type="submit" disabled={isLoading || !input.trim()}>
                  {isLoading ? 'Sending...' : 'Send'}
                </Button>
              </Group>
            </form>
          </Stack>
        </Box>
      </Paper>
    </Container>
  )
}

export default App
