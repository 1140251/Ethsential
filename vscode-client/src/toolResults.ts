export interface ToolCommandOutput {
  success: boolean;
  error: string | null | undefined;
  issues: ToolCommandIssues[] | null | undefined;
  duration: Number | undefined;
}

export interface ToolCommandIssues {
  severity: string;
  pattern: string;
  description: string;
  lines: Number[];
  function: string;
  contract: string;
}
