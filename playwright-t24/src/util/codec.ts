import { XMLParser, XMLValidator } from 'fast-xml-parser';

/** UTF-8 safe base64 (Cyrillic beneficiary names survive the round trip). */
export const b64encode = (s: string) => Buffer.from(s, 'utf8').toString('base64');
export const b64decode = (s: string) => Buffer.from(s, 'base64').toString('utf8');

const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: '@', removeNSPrefix: true });

/** Parse XML, throwing with the validator's line/col on malformed input. */
export function parseXml(xml: string): any {
  const ok = XMLValidator.validate(xml);
  if (ok !== true) throw new Error(`Malformed XML at ${ok.err.line}:${ok.err.col} ${ok.err.msg}`);
  return parser.parse(xml);
}

/** Dotted path lookup into parsed XML: get(doc, 'Document.FIToFICstmrCdtTrf.CdtTrfTxInf.PmtId.EndToEndId'). */
export function get(obj: any, path: string): any {
  return path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
}
