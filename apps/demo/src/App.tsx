import React from 'react'
import { useState } from 'react'
import { Container, Title, Text, Paper, Stack, Group, TextInput, Button, Box } from '@mantine/core'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const App = () => {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // TODO: Replace with actual SDK call
      // const response = await summit.query(input)

      // Mock response for now
      await new Promise((resolve) => setTimeout(resolve, 1000))
      const assistantMessage: Message = {
        role: 'assistant',
        content: `Mock response to: "${userMessage.content}"`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
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
                    <Text size="xs" opacity={0.6}>
                      {message.timestamp.toLocaleTimeString()}
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
            </Stack>
          )}
        </Box>

        <Box p="md" style={{ borderTop: '1px solid var(--mantine-color-gray-3)' }}>
          <form onSubmit={handleSubmit}>
            <Group gap="xs">
              <TextInput
                flex={1}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                disabled={isLoading}
              />
              <Button type="submit" disabled={isLoading || !input.trim()}>
                {isLoading ? 'Sending...' : 'Send'}
              </Button>
            </Group>
          </form>
        </Box>
      </Paper>
    </Container>
  )
}

export default App
