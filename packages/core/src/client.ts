export class SummitClient {
  private apiKey: string
  private baseUrl: string

  constructor(apiKey: string, baseUrl = 'http://localhost:8000') {
    this.apiKey = apiKey
    this.baseUrl = baseUrl
  }

  async query(text: string): Promise<any> {
    // TODO: Implement API call to /api/v1/query
    throw new Error('Not implemented yet')
  }

  async health(): Promise<{ status: string }> {
    // TODO: Implement API call to /api/v1/health
    throw new Error('Not implemented yet')
  }
}
