import type { ApiErrorCode } from './types';

/** Codes produced by the client itself in addition to the codes of the contract. */
export type ClientErrorCode = ApiErrorCode | 'NETWORK' | 'ABORTED' | 'BAD_RESPONSE';

export class ApiError extends Error {
  readonly status: number;
  readonly code: ClientErrorCode;
  readonly field: string | null;
  readonly retryAfter: number | null;
  readonly requestId: string | null;

  constructor(init: {
    status: number;
    code: ClientErrorCode;
    message: string;
    field?: string | null;
    retryAfter?: number | null;
    requestId?: string | null;
  }) {
    super(init.message);
    this.name = 'ApiError';
    this.status = init.status;
    this.code = init.code;
    this.field = init.field ?? null;
    this.retryAfter = init.retryAfter ?? null;
    this.requestId = init.requestId ?? null;
  }
}

/** A client-side hint per code, shown after the server message (ui-design §9). */
export const ERROR_HINTS: Partial<Record<ClientErrorCode, string>> = {
  INVALID_LENGTH: 'A tile has exactly 28 amino acids.',
  INVALID_CHARACTER: 'Use only the 20 standard one-letter amino-acid codes.',
  UNKNOWN_ACCESSION: 'Search for the protein by gene symbol or UniProt accession.',
  TILE_OUT_OF_RANGE: 'Choose a tile within the range stated above.',
  TILE_NOT_SCORABLE: 'Choose another tile of this protein.',
  MODEL_NOT_FOUND: 'Open the model page to see the available models.',
  RUN_NOT_FOUND: 'Check that the whole link, including the part after "#", was copied.',
  PAYLOAD_TOO_LARGE: 'Shorten the input.',
  NETWORK: 'Check your connection and try again.',
};
