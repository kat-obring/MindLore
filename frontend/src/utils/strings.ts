const leadingQuotes = /^[“”"']+/;
const trailingQuotes = /[“”"']+$/;

export const stripQuotes = (value: string) =>
  value.replace(leadingQuotes, "").replace(trailingQuotes, "");
