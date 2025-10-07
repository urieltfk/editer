import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export interface DocumentResponse {
  id: string
  share_id: string
  content: string
  created_at: string
  updated_at: string
}

export interface DocumentCreate {
  content: string
}

export interface DocumentUpdate {
  content: string
}

class DocumentApi {
  private baseURL = API_BASE_URL

  async getDocument(shareId: string): Promise<DocumentResponse> {
    const response = await axios.get(`${this.baseURL}/api/v1/documents/${shareId}`)
    return response.data
  }

  async createDocument(content: string): Promise<DocumentResponse> {
    const response = await axios.post(`${this.baseURL}/api/v1/documents`, {
      content
    })
    return response.data
  }

  async updateDocument(shareId: string, content: string): Promise<DocumentResponse> {
    const response = await axios.put(`${this.baseURL}/api/v1/documents/${shareId}`, {
      content
    })
    return response.data
  }
}

export const documentApi = new DocumentApi()
