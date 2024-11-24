import { Button, Checkbox, Chip, CircularProgress, FormControlLabel, Tooltip } from "@mui/material";
import FormBase from "@components/StatisticsView/form/FormBase/FormBase"
import { Stack } from "@mui/system";
import CustomTextField from "@src/components/Inputs/TextField";
import { useForm } from "@src/components/StatisticsView/form/Form.hook";
import FormExamples from "./FormBase/FormExamples";

const Form = () => {
    const { 
        form, 
        onFormUpdate, 
        onSubmit,
        isPendingStatsData,
        onSetGenerateReport
    } = useForm()

    return (
        <Stack 
            gap={2}
            flexDirection="column"
        >
            <FormExamples />
            <CustomTextField 
                margin="none"
                label="Titre"
                sx={{
                    maxWidth: 350
                }}
                value={form.title}
                onChange={(e) => onFormUpdate("title", e.target.value)}
            />
            <FormBase />
            <Stack
                justifyContent="flex-end"
                marginTop={4}
                flexDirection="row"
                gap={2}
            >
                <Tooltip title="Cette option permet de générer un rapport grace à l'IA. Attention ! Vous devez obligatoirement avoir une clé OpenAi pour bénéficier de cette fonctionnalité."><FormControlLabel 
                    control={<Checkbox onChange={(_, value) => onSetGenerateReport(value)} checked={form.generateReport} color="secondary" />} 
                    label="Rédiger un rapport" 
                /></Tooltip>
                <Button
                    variant="contained" 
                    onClick={onSubmit}
                    disabled={isPendingStatsData}
                    sx={{
                        minWidth: 150
                    }}
                >
                    {
                        !isPendingStatsData ?
                        "Générer"
                        :
                        <CircularProgress size={24} color="inherit" />
                    }
                    
                </Button>
            </Stack>
        </Stack>
    )
}


export default Form