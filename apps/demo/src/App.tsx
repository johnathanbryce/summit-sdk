import { useState } from 'react'
import { Container, Title, Text, Paper, Stack, Group, TextInput, Button, Box, SegmentedControl } from '@mantine/core'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
interface Message {
  role: 'user' | 'assistant'
  response: string
}

type InputType = 'summary' | 'chat'

const App = () => {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [inputType, setInputType] = useState<InputType>('summary')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      role: 'user',
      response: input.trim(),
    }
    setMessages((prev) => [...prev, userMessage])

    try {
      setIsLoading(true)
      const endpoint = inputType === 'chat' ? '/chat' : '/summarize'
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: [{ role: 'user', content: input }],
          respondInLanguage: null,
        }),
      })

      const data = await response.json()
      if (data.response) {
        setMessages((prevMessages) => [...prevMessages, data])
        setInput('')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Container size="md" py="xl">
      <Stack gap="lg" mb="xl" ta="center">
        <Title order={1}>Summit SDK Demo</Title>
        <Text c="dimmed">AI-powered content querying</Text>
      </Stack>

      <Paper shadow="sm" radius="md" withBorder>
        <Box
          h={500}
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
                  <Text size="sm">{message.response}</Text>
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
